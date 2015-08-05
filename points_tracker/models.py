from points_tracker.database import Model, SurrogatePK, Column, db, ReferenceCol, relationship

# models go here

class Audio(SurrogatePK, Model):
    __tablename__ = 'audio'
    name = Column(db.String(50), unique=False)
    length = Column(db.Integer, unique=False)  #stored in seconds
    filename = Column(db.String(32), unique=True)

    @property
    def tag_display(self):
        return ", ".join([tag.tag.lower() 
            for tag in self.tags if not tag.tag == self.name.upper()])
    
    def to_json(self):
        return dict(id=self.id,
                    name=self.name,
                    length=self.length,
                    tags=self.tag_display)

    def __repr__(self):
        return '<Audio %r>' % (self.name)


class AudioTag(SurrogatePK, Model):
    __tablename__ = 'audio_tags'
    tag = Column(db.String(50), unique=False)
    audio_id = Column(db.Integer, db.ForeignKey('audio.id'), nullable=False)
    audio = relationship('Audio', backref="tags")

    def __repr__(self):
        return '<Tag %r>' % (self.tag)
