from taggit.models import Tag, TaggedItem
from django.contrib.contenttypes.models import ContentType

ct_map = {}
for ct in ContentType.objects.using('doxypep_db').all():
    default_ct = ContentType.objects.using('default').get(
        app_label=ct.app_label,
        model=ct.model
    )
    ct_map[default_ct.id] = ct.id

print("Mapping:", ct_map)

copied = 0
skipped = 0
for item in TaggedItem.objects.using('default').all():
    if item.content_type_id not in ct_map:
        skipped += 1
        continue
    default_tag = Tag.objects.using('default').get(id=item.tag_id)
    doxypep_tag = Tag.objects.using('doxypep_db').get(slug=default_tag.slug)
    TaggedItem.objects.using('doxypep_db').get_or_create(
        object_id=item.object_id,
        content_type_id=ct_map[item.content_type_id],
        tag=doxypep_tag
    )
    copied += 1

print(f"Copied: {copied} | Skipped: {skipped}")
print(f"Total in doxypep_db: {TaggedItem.objects.using('doxypep_db').count()}")
