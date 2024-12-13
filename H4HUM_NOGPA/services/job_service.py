from models import db, Job
class JobService:
    @staticmethod
    def create_job(data):
        new_job = Job(title=data['title'], description=data['description'], domain=data['domain'])
        db.session.add(new_job)
        db.session.commit()
    @staticmethod
    def get_all_jobs():
        return Job.query.all()