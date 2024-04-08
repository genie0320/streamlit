# %%
from dotenv import load_dotenv
from pytube import YouTube
from youtube_transcript_api import YouTubeTranscriptApi
from google import generativeai as genai
from functools import lru_cache

# from IPython.display import display
# from IPython.display import Markdown

import textwrap
import re
from llamaIndex.prompts import new_prompt

load_dotenv()
genai.configure()


def get_source(url):
    res = {}
    res["source"] = YouTube(url)
    res["v_streams"] = (
        res["source"]
        .streams.filter(file_extension="mp4", progressive=True, type="video")
        .order_by("resolution")
        .desc()
    )
    res["a_streams"] = res["source"].streams.filter(type="audio").order_by("abr").desc()
    res["url"] = url
    return res


def get_id(obj):
    return obj.embed_url.split("/")[-1]


def get_itag(obj):
    """
    <Stream: itag="251" mime_type="audio/webm" abr="160kbps" acodec="opus" progressive="False" type="audio">
    <Stream: itag="22" mime_type="video/mp4" res="720p" fps="24fps" vcodec="avc1.64001F" acodec="mp4a.40.2" progressive="True" type="video">
    """
    tag = re.search(r'itag="(\d+)', str(obj)).group(1)
    extention = re.search(r'o/"(\d+)', str(obj)).group(1)
    return tag, extention


# def get_id(url):
#     # for url in urls:
#     if url.startswith("https://youtu.be"):
#         video_id = re.search(r"youtu\.be\/(\w+)", url).group(1)
#     elif url.startswith("https://www.youtube.com/watch?v"):
#         video_id = re.search(r"v=(\w+)", url).group(1)
#     return video_id


def get_video_info(url):
    """
    ({'title': "Google has the best AI now, but there's a problem...",
    'length': 235,
    'created': datetime.datetime(2024, 2, 23, 0, 0),
    'thumb': 'https://i.ytimg.com/vi/xPA0LFzUDiE/hq720.jpg',
    'video_stream': [<Stream: itag="18" mime_type="video/mp4" res="360p" fps="24fps" vcodec="avc1.42001E" acodec="mp4a.40.2" progressive="True" type="video">, <Stream: itag="22" mime_type="video/mp4" res="720p" fps="24fps" vcodec="avc1.64001F" acodec="mp4a.40.2" progressive="True" type="video">],
    'audio_stream': [],
    'chanel_id': 'UCsBjURrPoezykLs9EqgamOA'},
    <pytube.__main__.YouTube object: videoId=xPA0LFzUDiE>)
    """
    source = YouTube(url)
    yt_info = {}
    yt_info["title"] = source.title
    yt_info["length"] = source.length
    yt_info["created"] = source.publish_date
    yt_info["thumb"] = source.thumbnail_url
    yt_info["video_stream"] = source.streams.filter(
        file_extension="mp4", progressive=True, type="video"
    )
    yt_info["audio_stream"] = source.streams.filter(
        file_extension="mp4", progressive=True, type="audio"
    )
    yt_info["chanel_id"] = source.channel_id
    return yt_info, source


def yt_down(source, title):
    source.download(f"{title}.mp4", "download/")


def get_script(vid_id, langs=["ko", "en"]):

    transcript_list = YouTubeTranscriptApi.list_transcripts(vid_id)
    transcript = transcript_list.find_transcript(langs).fetch()
    script = "".join([script["text"] for script in transcript])
    return script


def get_summary(script):
    """
    models
    - models/gemini-1.0-pro
    - models/gemini-1.0-pro-001
    - models/gemini-1.0-pro-latest
    - models/gemini-1.0-pro-vision-latest
    - models/gemini-pro
    - models/gemini-pro-vision
    """
    model = genai.GenerativeModel("gemini-pro")

    genConfig = genai.types.GenerationConfig(
        # Only one candidate for now.
        candidate_count=1,
        stop_sequences=["x"],
        # max_output_tokens=4000,
        temperature=1.0,
    )

    prompt = """
    Summarize following youtube script 
    - Summarize the given text as 30% of the length of the original text.
    - Translate the result of summary into Korean.
    - Return only the translated summary.
    
    Script to summarize : {script}"
    """.format(
        script=script
    )

    response = model.generate_content(prompt, generation_config=genConfig, stream=False)

    return response.text


# def to_markdown(text):
#     text = text.replace("•", "  *")
#     return Markdown(textwrap.indent(text, "> ", predicate=lambda _: True))


def main():
    url = "https://youtu.be/xPA0LFzUDiE?si=-dgYEVwBCuKUah-Q"
    video_info = get_video_info(url)

    id = get_id(url)
    script = get_script(id)

    print(get_summary(script))


# %%
# if __name__ == "__main__":
#     main()


# %%

# import pathlib

# # %%
# script = "I talked to over 200 designers this islike the most cliche boring and sillyidea I'm using the human interface gucuz some clients might not be interestedin your mobile app designs atall how to know if your portfolio suckswell that's easy you can't just uploadit in there and wait for the emails tocome in you got to research and improveand today I'm going to show you exactlyhow to do it chances are you're notgoing to nail it the first time andthat's normal that's exactly how designworks I talked to over 200 designersthat have gotten their very first designjob in the last 12 months yes in thishorrible economy and there are somepatterns but what's more interesting ishow many of them succeeded with thefirst version of their portfolio youwant to guess the number it's prettyclose to zero so here's how to improveyour portfolio in a few easy step stepspeople viewing your portfolio won't havethe time to appreciate decorations ornice visuals of the website itself keepit simple and focused on presenting yourwork what we found out works best issimple black for wide backgrounds and areadable s serif font then write clearinformation about yourself and big juicythumbnails thumbnails are reallyimportant so we're going to go back tothumbnails later in this video and I'mgoing to show you how to use research tomake them better another thing isstructure you don't want a portfoliowhere you first need to click and enterthis website button or a view portfoliobutton no you want your projects to beon the very first page with nicebeautiful juicy thumbnails one thing Inoticed works really well and turnsheads is how you describe or title yourprojects I'm going to give you anexample of a dog walking app but pleasedon't make a dog walking app for yourportfolio this is like the most clicheboring and silly idea please don't do itbut assuming you already have you canjust write a dog walking app in a titleunder some screenshots the thumbnail oryou can write something like this makinglocal neighborhood dog walking bookingstwo times faster the first one isgeneric and boring the second one is waymore interesting because it shows thatyou understand that design is not aboutjust making some up it's about solving aproblem and of course saying things liketwo times faster or 40% biggerconversion for a fake portfolio projectis a bit over stretch obviously youcan't really test that data because theproduct is not real but that's okay it'snot supposed to be real it's supposed tobe about the goal that you had for thiswhole design project and the goal wasn'tto just make some dog walking up thegoal was to actually increase thoseconversions okay next one writing aboutyour skills avoid downplaying yourselfdon't write things like aspiring junioror beginner if you use those words it'spractically guaranteed that they'regoing to view you through the lens ofthese words so basically they're goingto think that you're pretty bad at whatyou do just say I'm a designer and don'twrite generic Bullit like I'm using thehuman interface guidelines to make humanCentric designs for the users this isjust gibberish and it's pretty stupidhere's a quick example on how you canmake it more relevant by bringingsomething more personal from your ownexperience into the description and I'mgoing to use it based on my ownexperiences but obviously don't justcopy that make one aboutyou when I was a kid I used to buildcomplex structures out of Lego blocksnow I'm using design blocks to makecomplex things a lot simpler make itpersonal and don't beboring all right time for the researchpart if you want to know what's going onwith your projects and with yourportfolio you need a dedicated websitenot a figma link not a be hands not adribble you need a website where you caninstall JavaScript tracking code codefrom sites like be usable or hot jarthere are many others to do yourresearch but you really really reallyneed those visual Analytics tool justGoogle analytics is not going to cut itbecause having visual analytics willallow you to actually see how people useyour site what they click on and moreimportantly what they don't click on nowhere's another tip if you're in designcommunities and by the way we have acommunity right here and you can join bysending me a DM if you're in thosecommunities there are great people therethat are very supportive they will helpyou they will try to guide you throughtheir own experiences and it's a prettygood idea to share your portfolio withthem but if you're using those websiteswith visual analytics turn them offbefore you let your friends andcolleagues give you feedback on yourside because it's likely that you don'treally need the recordings of the peoplethat are going to treat it differentlybecause they know and like you it'sreally good to reserve those 100 orcouple hundred free plan recordings forthe actual recruiters employers orclients it's not a problem if you canafford the paid plan in these tools butstill in that case split and segmentthose two groups so call one of themfriends and the other one my target youcan see some pretty interesting overlapbetween them but you can be sure thatyour target is going to spend way lesstime on your portfolio and it's going tobe way more negative about it that'snormal that's to be expected these aretwo different groups and you need totreat them as such I know the market istough and many recruiters don't even goto your portfolio but you need at least20 and optimally 50 people viewing yourportfolio to start analyzing therecordings and then look at what they doand optimize if they only click on onespecific project and skip the restoptimize the thumbnails and thedescriptions of those other ones if theydon't click on any of the projects justenter the portfolio scroll to theprojects and leave then you definitelyneed to change the thumbnails and thedescriptions another potential idea isto make multiple different portfolioswith slightly different projects orproject arrangement for specific typesof clients because some clients mightnot be interested in your mobile appdesign atall so yeah seeing those 200 plusdesigners succeed this year I realizedafter seeing their work that many of ushave forgotten how bad design is afoundation from which we grow into gooddesigners acknowledging that the badparts exist and we as humans are onlyhuman and we make mistakes this is theonly way for us to learn and not thinkthat the market or the reality around usis unfair because nobody clicks on ourprojects no it's likely because we didsomething wrong so I am putting all ofthese learnings and more into somethingI call the bad design course it willcover both all the portfolio tips fromthe successful designers all the ATScompliant resumés and a lot of thedesign parts that are still being donewrong by Juniors because you can have abeautiful UI with horrible informationarchitecture and really bad ux so we'regoing to go through all of those reallybad examples so you know what to avoidand what to do to correct them thecourse drops late to Mid April and theprice in the pre-order now is $39 it'sgoing to be 80 so practically doublewhen the course goes live and it's goingto be $10 more one week from this videoso if you want it the cheapest get itnow if you want to support me and pay mea little bit more then just wait untilit's released okay so why is it calledthe bad design course it's a bit likereverse psychology because we need tounderstand the bad things to be able toidentify them and avoid them in theFuture Link in the description now usewhat you learned in this video and fixup your portfolio so we both can have abeautiful day"

# model.count_tokens(script)

# # %%
