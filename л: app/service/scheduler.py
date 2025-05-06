import pickle
from datetime import datetime

from apscheduler.events import JobEvent, EVENT_JOB_REMOVED, EVENT_JOB_MODIFIED
from apscheduler.jobstores.base import JobLookupError
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.schedulers.base import STATE_STOPPED, STATE_RUNNING
from apscheduler.util import datetime_to_utc_timestamp
from sqlalchemy import bindparam


class CustomScheduler(AsyncIOScheduler):
    def remove_jobs(self, job_ids, jobstore=None):
        jobstore_alias = None
        with self._jobstores_lock:
            # Check if the job is among the pending jobs
            if self.state == STATE_STOPPED:
                for i, (job, alias, replace_existing) in enumerate(self._pending_jobs):
                    if job.id in job_ids and jobstore in (None, alias):
                        del self._pending_jobs[i]
                        jobstore_alias = alias
                        break
            else:
                # Otherwise, try to remove it from each store until it succeeds or we run out of
                # stores to check
                for alias, store in self._jobstores.items():
                    if jobstore in (None, alias):
                        try:
                            store.remove_jobs(job_ids)
                            jobstore_alias = alias
                            break
                        except JobLookupError:
                            continue

        if jobstore_alias is None:
            raise JobLookupError(job_ids)

        # Notify listeners that a job has been removed
        for job_id in job_ids:
            event = JobEvent(EVENT_JOB_REMOVED, job_id, jobstore_alias)
            self._dispatch_event(event)

            self._logger.info("Removed job %s", job_id)

    def custom_reschedule(
        self, job_id, job_id_to_trigger, trigger=None, **trigger_args
    ):

        trigger = self._create_trigger(trigger, trigger_args)
        now = datetime.now(self.timezone)
        next_run_time = trigger.get_next_fire_time(None, now)

        job = self.modify_job(job_id, trigger=trigger, next_run_time=next_run_time)
        job_id_to_trigger[job_id] = {"next_run_time": next_run_time, "job": job}

    def reschedule_jobs(self, job_id_to_trigger_args):
        job_id_to_trigger = {}
        for job_id, values in job_id_to_trigger_args.items():
            self.custom_reschedule(
                job_id=job_id,
                job_id_to_trigger=job_id_to_trigger,
                trigger="cron",
                **values
            )
        with self._jobstores_lock:
            self._lookup_jobstore("default").modify_jobs(job_id_to_trigger)

    def modify_job(self, job_id, jobstore=None, **changes):
        with self._jobstores_lock:
            job, jobstore = self._lookup_job(job_id, jobstore)
            job._modify(**changes)
        self._dispatch_event(JobEvent(EVENT_JOB_MODIFIED, job_id, jobstore))

        # Wake up the scheduler since the job's next run time may have been changed
        if self.state == STATE_RUNNING:
            self.wakeup()

        return pickle.dumps(job.__getstate__(), 5)


def dateadd(date_field, interval):
    return date_field + interval


class CustomJobStore(SQLAlchemyJobStore):
    def remove_jobs(self, job_ids):
        delete = self.jobs_t.delete().where(self.jobs_t.c.id.in_(job_ids))
        with self.engine.begin() as connection:
            result = connection.execute(delete)
            if result.rowcount == 0:
                raise JobLookupError(job_ids)

    def modify_jobs(self, job_id_to_changes):

        values = [
            {
                "_id": job_id,
                "next_run_time": datetime_to_utc_timestamp(value["next_run_time"]),
                "job_state": value["job"],
            }
            for job_id, value in job_id_to_changes.items()
        ]

        stmt = (
            self.jobs_t.update()
            .where(self.jobs_t.c.id == bindparam("_id"))
            .values(
                next_run_time=bindparam("next_run_time"),
                job_state=bindparam("job_state"),
            )
        )
        with self.engine.begin() as connection:
            result = connection.execute(stmt, values)
            if result.rowcount == 0:
                raise JobLookupError(job_id_to_changes.keys())


jobstores = {"default": CustomJobStore(url="sqlite:///dbs.sqlite3")}
scheduler = CustomScheduler(jobstores=jobstores)

===
Конец файла ===