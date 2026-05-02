from django.contrib import admin
from .models import Message

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    # Admin irratti eenyu eenyuuf akka barreesse agarsiisa
    list_display = ('sender', 'receiver', 'content_preview', 'timestamp', 'is_read')
    
    # Namoota ergaa waliif ergan qofaan addaan qooduuf (Filter)
    list_filter = ('is_read', 'timestamp', 'sender')
    
    # Ergaa keessa jiru barbaaduuf
    search_fields = ('content', 'sender__username', 'receiver__username')

    # Smart function: Ergaa dheeraa gabaabsitee Admin irratti ilaaluuf
    def content_preview(self, obj):
        if len(obj.content) > 50:
            return obj.content[:50] + "..."
        return obj.content
    content_preview.short_description = 'Ergaa'