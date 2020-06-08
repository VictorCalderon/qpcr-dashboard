from qpcr_manager.extensions import db


class Result(db.Model):
    """Base Results Model
    """

    __tablename__ = 'results'

    id = db.Column(db.Integer, primary_key=True)
    amp_status = db.Column(db.Boolean)
    amp_cq = db.Column(db.Float)
    cq_confidence = db.Column(db.Float)

    sample_id = db.Column(db.Integer, db.ForeignKey('samples.id'))
    marker_id = db.Column(db.Integer, db.ForeignKey('markers.id'))
    sample = db.relationship('Sample', backref='results', lazy=True)

    def __repr__(self):
        return '<Result: {}>'.format(self.id)
