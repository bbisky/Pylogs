from django.contrib import admin
import os
from django.conf import settings
from models import Category, Comments, Links,Post, Tags, Setting

MEDIA_URL = settings.MEDIA_URL
if not MEDIA_URL.endswith("/"): MEDIA_URL +=  "/"
    

class TagsAdmin(admin.ModelAdmin):
    list_display = ('name','slug','reference_count')
    search_fields = ['name']
    
class PostAdmin(admin.ModelAdmin):
    list_display = ('title','get_cat_str','pubdate','hits')
    search_fields = ['title']
    list_filter =('post_type','category')
    fieldsets = (
    (None, {
        'fields': ('title', 'post_name','category','post_type','markup',
                   'content','tags','post_status','comment_status',)
    }),
    ('Advanced options', {
        'classes': ('collapse',),
        'fields': ('post_parent','menu_order')
    }),
    )
    class Media:
        js = (
                os.path.join(MEDIA_URL,'js/tiny_mce/tiny_mce.js'),
                os.path.join(MEDIA_URL,'js/admin_textarea.js'),
            )
    def save_model(safe,request,obj,form,change):
        #update tag reference_count
        if change:
            tag_ids_before_save = set([tag.id for tag in obj.tags.all()])
            obj.save()
            form.save_m2m()
            tag_ids_after_save = set([tag.id for tag in obj.tags.all()])
            need_update_tag_ids = tag_ids_after_save.symmetric_difference(tag_ids_before_save)
            for tag_id in need_update_tag_ids:
                tag = Tags.objects.get(id__exact = tag_id)
                tag.reference_count = tag.post_set.count()
                tag.save()
        else:
            obj.save()
            form.save_m2m()
            if obj.tags:
                all_tags =  obj.tags.all()
                for tag in all_tags:
                    tag.reference_count = tag.post_set.count()
                    tag.save()      
            
            

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name','desc')
    search_fields = ['name']

class CommentsAdmin(admin.ModelAdmin):
    list_filter =('comment_approved',)
    list_display = ('comment_author','comment_author_email',
                    'comment_date','comment_approved','comment_author_IP','comment_agent')
    search_fields = ['comment_author']
    
class LinksAdmin(admin.ModelAdmin):
    list_display = ('link_title','link_url')
    fieldsets = (
        (None, {
            'fields': ('link_title','link_url','link_order')
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('link_desc', 'link_image')
        }),
    )

class SettingAdmin(admin.ModelAdmin):
    list_display = ('setting_name','setting_desc','setting_value')
  
admin.site.register(Tags,TagsAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Comments,CommentsAdmin)
admin.site.register(Links,LinksAdmin)
admin.site.register(Post,PostAdmin)   
admin.site.register(Setting,SettingAdmin)