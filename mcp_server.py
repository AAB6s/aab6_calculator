import sys,os,django
from mcp.server.fastmcp import FastMCP
from asgiref.sync import sync_to_async

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE","firstproject.settings")
django.setup()

from ConferenceApp.models import Conference
from SessionApp.models import Session

mcp=FastMCP("Conference Assistant")

@mcp.tool()
async def list_conferences()->str:
    @sync_to_async
    def q():return list(Conference.objects.all())
    x=await q()
    return "No conferences found." if not x else "\n".join([f"- {c.name} ({c.start_date} to {c.end_date})" for c in x])

@mcp.tool()
async def get_conference_details(name:str)->str:
    @sync_to_async
    def q():
        try:return Conference.objects.get(name__icontains=name)
        except Conference.DoesNotExist:return None
        except Conference.MultipleObjectsReturned:return"MULTIPLE"
    c=await q()
    if c=="MULTIPLE":return f"Multiple conferences match '{name}'."
    if not c:return f"Conference '{name}' not found."
    return f"Name: {c.name}\nTheme: {c.get_theme_display()}\nLocation: {c.location}\nDates: {c.start_date} to {c.end_date}\nDescription: {c.description}"

@mcp.tool()
async def list_sessions(conference_name:str)->str:
    @sync_to_async
    def q():
        try:
            conf=Conference.objects.get(name__icontains=conference_name)
            return list(conf.sessions.all()),conf
        except Conference.DoesNotExist:return None,None
        except Conference.MultipleObjectsReturned:return"MULTIPLE",None
    res,conf=await q()
    if res=="MULTIPLE":return f"Multiple conferences match '{conference_name}'."
    if conf is None:return f"Conference '{conference_name}' not found."
    if not res:return f"No sessions found for conference '{conf.name}'."
    return "\n".join([f"- {s.title} ({s.start_time}-{s.end_time}) in {s.room}\n  Topic: {s.topic}" for s in res])

@mcp.tool()
async def filter_conferences_by_theme(theme:str)->str:
    @sync_to_async
    def q():return list(Conference.objects.filter(theme__icontains=theme))
    x=await q()
    return f"No conferences found with theme '{theme}'." if not x else "\n".join([f"- {c.name} ({c.location})" for c in x])

if __name__=="__main__":mcp.run(transport="stdio")