from points_tracker.models import AudioTag

## converts tags with commas in them to individual tags
def clean_tags(tag_ids):
	for tag in AudioTag.query.all():
		if "," in tag.tag:
			tags = tag.tag.split(",")
			for tag_string in tags:
				AudioTag(tag=tag_string,
					     audio_id=tag.audio_id).save()
			tag.delete()