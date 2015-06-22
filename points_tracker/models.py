from points_tracker.database import Model, SurrogatePK, Column, db, ReferenceCol, relationship

# models go here

class Audio(SurrogatePK, Model):
    __tablename__ = 'audio'
    name = Column(db.String(50), unique=False)
    length = Column(db.Integer, unique=False)  #stored in seconds
    filename = Column(db.String(32), unique=False)

    def __repr__(self):
        return '<Audio %r>' % (self.name)


class AudioTag(SurrogatePK, Model):
    __tablename__ = 'audio_tags'
    tag = Column(db.String(50), unique=False)
    audio = Column(db.Integer, db.ForeignKey("audio.id"), nullable=False)

    def __repr__(self):
        return '<Tag %r>' % (self.tag)


class AudioGroup(SurrogatePK, Model):
    __tablename__ = 'audio_groups'
    name = Column(db.String(50), unique=False)
    audio = Column(db.Integer, db.ForeignKey("audio.id"), nullable=False)

    def __repr__(self):
        return '<Group %r>' % (self.name)
