from qpcr_manager.extensions import db


class Sample(db.Model):
    """Base Sample Model
    """

    __tablename__ = 'samples'

    id = db.Column(db.Integer, primary_key=True)
    sample = db.Column(db.String, nullable=False)
    description = db.Column(db.Text)
    location = db.Column(db.String)
    latitude = db.Column(db.Float)
    longitiude = db.Column(db.Float)

    experiment_id = db.Column(db.Integer, db.ForeignKey(
        'experiments.id', ondelete='CASCADE'))

    experiment = db.relationship(
        'Experiment', backref='samples', cascade='all,delete', lazy=True)

    def __repr__(self):
        return '<Sample: {}>'.format(self.id)
