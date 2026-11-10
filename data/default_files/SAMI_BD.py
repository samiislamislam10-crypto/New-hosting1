# ═══════════════════════════════════════════════════════════════
#███████╗ █████╗ ███╗   ███╗██╗
#██╔════╝██╔══██╗████╗ ████║██║
#███████╗███████║██╔████╔██║██║
#╚════██║██╔══██║██║╚██╔╝██║██║
#███████║██║  ██║██║ ╚═╝ ██║██║
#╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝

#          S A M I   B D
#
#        ★ SAMI BD — প্রিমিয়াম অল-ইন-ওয়ান TCP বট ★
#        ▌ লগইন ইঞ্জিন + বট কোর + মূল এন্ট্রি ▌
#        ▌ শুধু এই একটি ফাইল রান করুন ▌
#        ▌ .S1 - .S11 সম্পূর্ণ ফিচার যুক্ত ▌
# ═══════════════════════════════════════════════════════════════

import asyncio
import random
import json
import os
import time
import sys
import uuid
from datetime import datetime

import aiohttp
import httpx
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from google_play_scraper import app as play_scraper
from protobuf_decoder.protobuf_decoder import Parser

try:
    from cfonts import render
    _HAS_CFONTS = True
except Exception:
    _HAS_CFONTS = False
    def render(text, colors=None, align=None):
        return text

# ─── গেম-নির্দিষ্ট মডিউল ───
from xC4 import *
from xP import JoinSq, OpenCh, MsqSq, ExitSq
from byte import Encrypt_ID, encrypt_api
from Pb2 import (
    DEcwHisPErMsG_pb2,
    sQ_pb2,
    MajoRLoGinrEs_pb2,
    PorTs_pb2,
    MajoRLoGinrEq_pb2,
)

# ─── কনফিগ ফাইল (UID / PW / REGION / ADMIN) ───
from main import UID, PW, REGION_PREF, ADMIN_UID

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# ═══════════════════════════════════════════════════════════════
#                    ★ প্রিমিয়াম কনসোল ডিজাইন ★
# ═══════════════════════════════════════════════════════════════

C = {
    "reset": "\033[0m",
    "bold": "\033[1m",
    "dim": "\033[2m",
    "cyan": "\033[1;36m",
    "green": "\033[1;32m",
    "yellow": "\033[1;33m",
    "red": "\033[1;31m",
    "magenta": "\033[1;35m",
    "white": "\033[1;37m",
    "gray": "\033[1;90m",
    "blue": "\033[1;34m",
    "pink": "\033[1;95m",
    "orange": "\033[38;5;208m",
    "purple": "\033[38;5;129m",
    "gold": "\033[38;5;220m",
    "mint": "\033[38;5;121m",
}


def c(text, color):
    return f"{C.get(color, '')}{text}{C['reset']}"


def log(level, msg):
    icons = {
        "তথ্য":  ("cyan",    "ℹ"),
        "সফল":  ("green",   "✔"),
        "অপেক্ষা":("yellow", "◌"),
        "সতর্ক": ("orange",  "⚠"),
        "ত্রুটি": ("red",     "✘"),
        "বট":    ("magenta", "★"),
        "নেট":   ("blue",    "⇄"),
        "অথেন":  ("gold",    "🔑"),
        "চ্যাট": ("pink",    "💬"),
        "কমান্ড":("mint",    "⚡"),
    }
    color, icon = icons.get(level, ("white", "•"))
    ts = time.strftime("%H:%M:%S")
    tag = f"{c(f'[{ts}]', 'gray')} {c(f'{icon} {level}', color)}"
    print(f" {tag} {c('│', 'gray')} {msg}")


def print_banner():
    banner = render('SAMI BD', colors=['red', 'yellow'], align='center')
    sub    = render('PREMIUM TCP BOT', colors=['cyan', 'magenta'], align='center')
    print()
    print(c("╔" + "═" * 62 + "╗", "magenta"))
    print(c("║", "magenta") + c(" " * 62, "magenta") + c("║", "magenta"))
    print(c("║", "magenta") + banner.center(70) + c("║", "magenta"))
    print(c("║", "magenta") + sub.center(68) + c("║", "magenta"))
    print(c("║", "magenta") + c(" " * 62, "magenta") + c("║", "magenta"))
    print(c("║", "magenta") + c("▌ তৈরি ও পরিচালনায় — SAMI BD ▌".center(62), "gold") + c("║", "magenta"))
    print(c("╚" + "═" * 62 + "╝", "magenta"))
    print()


def print_line(title, value, icon="➤"):
    print(f"  {c(icon, 'cyan')}  {c(f'{title:<12}', 'white')} {c('›', 'gray')} {c(str(value), 'gold')}")


def print_box(title, lines, color="magenta"):
    if isinstance(lines, dict):
        lines = [f"{c(k, 'white')} {c('›', 'gray')} {c(v, 'green')}" for k, v in lines.items()]
    elif isinstance(lines, list) and lines and isinstance(lines[0], tuple):
        lines = [f"{c(k, 'white')} {c('›', 'gray')} {c(v, 'green')}" for k, v in lines]
    width = 56
    print()
    print(c(f"┌{'─' * width}┐", color))
    print(c("│", color) + c(f"  {title.center(width - 4)}  ", "gold") + c("│", color))
    print(c(f"├{'─' * width}┤", color))
    for line in lines:
        print(c("│", color) + f"  {line:<{width - 2}} " + c("│", color))
    print(c(f"└{'─' * width}┘", color))
    print()


def print_divider(char="─", color="gray", width=62):
    print(c(char * width, color))


def print_tag(text, color="cyan"):
    print(f"  {c('▸', color)} {c(text, color)}")


# ═══════════════════════════════════════════════════════════════
#                    ★ গ্লোবাল ভেরিয়েবল ★
# ═══════════════════════════════════════════════════════════════

online_writer = None
whisper_writer = None
bot_uid = None
ToKen = None
region = None
bot_nickname = "SAMI BD"
bot_clan_id = 0
admin_uid = ADMIN_UID   # ✅ config থেকে আসছে

evo_cycle_running = False
evo_cycle_task = None
bot_enabled = True

EVO_IDS = [
    909000063, 909000075, 909040010, 909000081, 909039011,
    909045001, 909038012, 909042008, 909051003, 909035012,
    909000098, 909033002, 909037011, 909049010, 909041005,
    909038010, 909033001, 909035007, 909000090, 909000085,
    909000068
]

AES_KEY = b'Yg&tc%DEuh6%Zc^8'
AES_IV  = b'6oyZDr22E3ychjM%'

BADGE_VALUES = {
    "s1": 1048576,
    "s2": 32768,
    "s3": 2048,
    "s4": 64,
    "s5": 262144,
}

REGION_LANG = {
    "BD": "bn", "IND": "hi", "PK": "ur", "SG": "en", "ID": "id",
    "ME": "ar", "VN": "vi", "TW": "zh", "CIS": "ru", "TH": "th",
    "EU": "en", "US": "en", "SAC": "es", "LK": "en", "BR": "pt",
}

DEFAULT_HEADERS = {
    'User-Agent': 'UnityPlayer/2018.4.12f1 (UnityWebRequest/1.0, libcurl/8.5.0-DEV)',
    'Connection': 'Keep-Alive',
    'Accept-Encoding': 'gzip',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Expect': '100-continue',
    'X-Unity-Version': '2018.4.12f1',
    'X-GA-SV': '1789535859',
    'X-GA': 'v1 1',
    'ReleaseVersion': 'OB55',
}


# ═══════════════════════════════════════════════════════════════
#              ★ ইমোট লোডিং ★
# ═══════════════════════════════════════════════════════════════

try:
    with open("emotes.json", "r", encoding="utf-8") as _f:
        _emote_list = json.load(_f)

    GENERAL_EMOTES_MAP = {}
    EMOTE_MAP = {}
    for item in _emote_list:
        num_str = str(item["Number"]).strip()
        emote_id = int(item["Id"])
        GENERAL_EMOTES_MAP[num_str] = emote_id
        GENERAL_EMOTES_MAP[num_str.lower()] = emote_id
        if num_str.isdigit():
            EMOTE_MAP[int(num_str)] = emote_id

    print_tag(f"ইমোট লোড হয়েছে: {len(GENERAL_EMOTES_MAP)} টি (নাম্বার: {len(EMOTE_MAP)})", "green")
except Exception as _e:
    GENERAL_EMOTES_MAP = {}
    EMOTE_MAP = {}
    print_tag(f"ইমোট লোড ব্যর্থ হয়েছে: {_e}", "red")

NAME_EMOTES = {
    "ak": 909000063, "scar": 909000068, "mp40": 909000075,
    "m1014": 909000081, "xm8": 909000085, "famas": 909000090,
    "ump": 909000098, "m1887": 909035007, "woodpecker": 909042008,
    "groza": 909041005, "m4a1": 909033001, "thompson": 909038010,
    "g18": 909038012, "parafal": 909045001, "p90": 909049010,
    "m60": 909051003, "fist": 909037011, "ring": 909050009,
    "heart": 909038004, "love": 909000010, "dance": 909000027,
    "hello": 909000001, "hi": 909000001, "money": 909000129,
    "lol": 909000002, "sad": 909038005, "angry": 909000014,
    "chicken": 909000006, "dab": 909000005, "selfie": 909000040,
    "shower": 909051004, "flower": 909051002, "petals": 909051013,
}


# ═══════════════════════════════════════════════════════════════
#              ★ প্রোটোবাফ হেল্পার ★
# ═══════════════════════════════════════════════════════════════

def _pb_varint(n):
    if n < 0:
        n = (1 << 64) + n
    out = bytearray()
    while True:
        b = n & 0x7F
        n >>= 7
        if n:
            b |= 0x80
        out.append(b)
        if not n:
            break
    return bytes(out)


def _pb_tag(f, w):
    return _pb_varint((f << 3) | w)


def _pb_field(f, v):
    if isinstance(v, bool):
        v = int(v)
    if isinstance(v, int):
        return _pb_tag(f, 0) + _pb_varint(v)
    if isinstance(v, str):
        d = v.encode('utf-8')
        return _pb_tag(f, 2) + _pb_varint(len(d)) + d
    if isinstance(v, (bytes, bytearray)):
        d = bytes(v)
        return _pb_tag(f, 2) + _pb_varint(len(d)) + d
    return b""


def get_proto_field(d, key, default=None):
    if not d or not isinstance(d, dict):
        return default
    if key in d:
        return d[key].get('data', default)
    if str(key) in d:
        return d[str(key)].get('data', default)
    return default


async def parse_results(parsed_results):
    result_dict = {}
    for result in parsed_results:
        field_data = {"wire_type": result.wire_type}
        if result.wire_type in ("varint", "string", "bytes"):
            field_data["data"] = result.data
        elif result.wire_type == "length_delimited":
            if hasattr(result.data, "results"):
                field_data["data"] = await parse_results(result.data.results)
            elif isinstance(result.data, list):
                field_data["data"] = await parse_results(result.data)
            else:
                field_data["data"] = str(result.data)
        result_dict[str(result.field)] = field_data
    return result_dict


# ═══════════════════════════════════════════════════════════════
#              ★ AES হেল্পার ★
# ═══════════════════════════════════════════════════════════════

async def aes_encrypt(payload, key, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return cipher.encrypt(pad(payload, AES.block_size))


async def encrypt_packet(packet_hex, key, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    packet_bytes = bytes.fromhex(packet_hex)
    padded_packet = pad(packet_bytes, AES.block_size)
    return cipher.encrypt(padded_packet).hex()


# ═══════════════════════════════════════════════════════════════
#              ★ লগইন ইঞ্জিন ★
# ═══════════════════════════════════════════════════════════════

async def get_playstore_version():
    loop = asyncio.get_event_loop()
    try:
        res = await loop.run_in_executor(
            None,
            lambda: play_scraper('com.dts.freefireth', lang='hi', country='id'),
        )
        return res.get("version", "1.132.8")
    except Exception:
        return "1.132.8"


async def version_config(client_http, region="IND"):
    app_version = await get_playstore_version()
    lang = REGION_LANG.get(region, "hi")
    api_url = (
        f"https://version.ggwhitehawk.com/live/ver.php?version={app_version}"
        f"&lang={lang}&device=android&channel=android&appstore=googleplay"
        f"&region={region}&whitelist_version=1.3.0&whitelist_sp_version=1.0.0"
    )
    try:
        res = await client_http.get(api_url)
        data = res.json()
        return (
            data.get("latest_release_version"),
            data.get("remote_version"),
            data.get("server_url"),
        )
    except Exception:
        return None


async def get_access_token(client_http, uid, password):
    url = "https://100067.connect.garena.com/oauth/guest/token/grant"
    hdrs = {
        "Host": "100067.connect.garena.com",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 12; SM-G998B Build/SP1A.210812.016)",
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "close",
    }
    data = {
        "uid": str(uid),
        "password": str(password),
        "response_type": "token",
        "client_type": "2",
        "client_secret": "2ee44819e9b4598845141067b281621874d0d5d7af9d8f7e00c1e54715b7d1e3",
        "client_id": "100067",
    }
    for attempt in range(3):
        try:
            r = await client_http.post(url, headers=hdrs, data=data)
            if r.status_code == 200:
                rd = r.json()
                return rd.get("open_id"), rd.get("access_token"), rd.get("platform", 4)
        except Exception:
            pass
        await asyncio.sleep(0.5)
    return None


async def build_majorlogin_payload(open_id, access_token, platform, client_version):
    try:
        proto = MajoRLoGinrEq_pb2.MajorLogin()
        proto.event_time = str(datetime.now())[:-7]
        proto.game_name = "free fire"
        proto.platform_id = 1
        proto.client_version = str(client_version)
        proto.client_version_code = "2019121229"
        proto.system_software = "Android OS 15 / API-35 (AP3A.240905.015.A2/185014)"
        proto.system_hardware = "Handheld"
        proto.device_type = "Handheld"
        proto.screen_width = 1600
        proto.screen_height = 719
        proto.screen_dpi = "234"
        proto.processor_details = "ARM64 FP ASIMD AES | 1820 | 8"
        proto.memory = 2798
        proto.gpu_renderer = "Mali-G57"
        proto.gpu_version = "OpenGL ES 3.2 v1.r49p1-04eac0.2848c17a2fd4e9340e06555168eaa3c9"
        proto.unique_device_id = f"Google|{str(uuid.uuid4())}"
        proto.client_ip = f"{random.randint(103,223)}.{random.randint(10,250)}.{random.randint(10,250)}.{random.randint(10,250)}"
        proto.language = "hi"
        proto.open_id = str(open_id)
        proto.open_id_type = "4"
        proto.login_open_id_type = 4
        proto.access_token = str(access_token)
        proto.login_by = 2
        proto.platform_sdk_id = 1
        proto.origin_platform_type = "4"
        proto.primary_platform_type = "4"
        proto.reg_avatar = 1
        proto.channel_type = 3
        proto.telecom_operator = "JIO"
        proto.network_operator_a = "JIO"
        proto.network_type = "WIFI"
        proto.network_type_a = "WIFI"
        proto.cpu_type = 2
        proto.cpu_architecture = "64"
        proto.graphics_api = "OpenGLES2"
        proto.supported_astc_bitset = 8191
        proto.client_using_version = "7428b253defc164018c604a1ebbfebdf"
        proto.loading_time = 15078
        proto.release_channel = "android"
        proto.extra_info = "KqsHTx3+QOmBRR1WKvaWewlcpqJBfjki+PPHQoQG8+0yV+Uos7gUFFjHMQ/e7u6han6Fl77r7c3vMN3p8UbKgN+nfycQCgwBmWgBzomx2gj84c+p"
        proto.android_engine_init_flag = 111207
        proto.if_push = 1
        proto.is_vpn = 0
        proto.memory_available.version = 55
        proto.memory_available.hidden_value = 81
        proto.external_storage_total = 49973
        proto.external_storage_available = 11338
        proto.internal_storage_total = 854
        proto.internal_storage_available = 11466
        proto.game_disk_storage_total = 49973
        proto.game_disk_storage_available = 11466
        proto.external_sdcard_total_storage = 49973
        proto.external_sdcard_avail_storage = 11466
        proto.library_path = "/data/app/~~lHFxTCCbupG2QVJmsURtZw==/com.dts.freefireth-N3aCHpHNXpdxjD80uIIbww==/lib/arm64"
        proto.library_token = "b8e0cd5e295eee42f5860d3c86e483dd|/data/app/~~lHFxTCCbupG2QVJmsURtZw==/com.dts.freefireth-N3aCHpHNXpdxjD80uIIbww==/base.apk"

        base_payload = proto.SerializeToString()

        extra = b""
        extra += _pb_field(96, '{"cur_rate":[90,60,120],"support_etc2":false}')
        extra += _pb_field(97, 1)
        extra += _pb_field(99, "4")
        extra += _pb_field(100, "4")
        extra += _pb_field(102, b"\x17]ENWU\x0eR5")
        extra += _pb_field(104, 52882)
        extra += _pb_field(105, 1)
        extra += _pb_field(106, "https://dl.ak.freefiremobile.com/live/ABHotUpdates/|https://core-ak.freefiremobile.com/live/ABHotUpdates/|6b2078db9d22dd98f8e9386a39af8462")
        extra += _pb_field(107, "c8e41b7a93f02d56e1a94c7b8203f5d1")

        return await aes_encrypt(base_payload + extra, AES_KEY, AES_IV)
    except Exception as e:
        log("ত্রুটি", f"পেলোড তৈরিতে সমস্যা: {e}")
        return None


async def send_majorlogin(client_http, data, release_version, server_url):
    try:
        url = f"{server_url}MajorLogin" if server_url.endswith('/') else f"{server_url}/MajorLogin"
        req_headers = DEFAULT_HEADERS.copy()
        req_headers["ReleaseVersion"] = str(release_version)

        response = await client_http.post(url, headers=req_headers, data=data)
        if response.status_code != 200 or len(response.content) < 40:
            return None

        res_proto = MajoRLoGinrEs_pb2.MajorLoginRes()
        try:
            res_proto.ParseFromString(response.content)
        except Exception:
            pass

        if not (res_proto.account_uid and res_proto.token):
            for offset in range(min(128, len(response.content))):
                try:
                    cc = MajoRLoGinrEs_pb2.MajorLoginRes()
                    cc.ParseFromString(response.content[offset:])
                    if cc.account_uid and cc.token:
                        res_proto = cc
                        break
                except Exception:
                    pass

        parsed = Parser().parse(response.content.hex())
        dict_res = await parse_results(parsed)

        key_val = get_proto_field(dict_res, 22) or res_proto.key or AES_KEY
        iv_val  = get_proto_field(dict_res, 23) or res_proto.iv  or AES_IV

        if isinstance(key_val, str):
            try: key_val = bytes.fromhex(key_val)
            except Exception: pass
        if isinstance(iv_val, str):
            try: iv_val = bytes.fromhex(iv_val)
            except Exception: pass

        res_proto.key = key_val
        res_proto.iv  = iv_val
        if not res_proto.url:
            res_proto.url = server_url
        return res_proto
    except Exception as e:
        log("ত্রুটি", f"MajorLogin সমস্যা: {e}")
        return None


async def send_getlogin(client_http, data, base_url, token, release_version):
    try:
        url = f"{base_url.rstrip('/')}/GetLoginData"
        req_headers = DEFAULT_HEADERS.copy()
        req_headers["ReleaseVersion"] = str(release_version)
        req_headers['Authorization'] = f"Bearer {token}"

        response = await client_http.post(url, headers=req_headers, data=data)
        if response.status_code != 200:
            return None

        res_proto = PorTs_pb2.GetLoginData()
        try:
            res_proto.ParseFromString(response.content)
        except Exception:
            pass

        parsed = Parser().parse(response.content.hex())
        dict_res = await parse_results(parsed)
        return res_proto, dict_res
    except Exception as e:
        log("ত্রুটি", f"GetLoginData সমস্যা: {e}")
        return None


async def do_login(uid, password, region_pref="IND"):
    async with httpx.AsyncClient(verify=False, timeout=15.0) as client_http:
        log("নেট", "ভার্সন কনফিগারেশন আনা হচ্ছে ...")
        vc = await version_config(client_http, region_pref)
        if not vc:
            log("ত্রুটি", "ভার্সন কনফিগ ব্যর্থ হয়েছে।")
            return None
        release_version, client_version, server_url = vc
        log("সফল", f"ভার্সন: {client_version} │ রিলিজ: {release_version}")

        log("নেট", "অ্যাক্সেস টোকেন আনা হচ্ছে ...")
        tg = await get_access_token(client_http, uid, password)
        if not tg:
            log("ত্রুটি", "UID বা পাসওয়ার্ড ভুল — অ্যাক্সেস টোকেন পাওয়া যায়নি।")
            return None
        open_id, access_token, platform = tg
        log("সফল", "অ্যাক্সেস টোকেন সফলভাবে পাওয়া গেছে।")

        log("তথ্য", "MajorLogin পেলোড তৈরি হচ্ছে ...")
        payload = await build_majorlogin_payload(open_id, access_token, platform, client_version)
        if not payload:
            log("ত্রুটি", "পেলোড তৈরি ব্যর্থ হয়েছে।")
            return None

        log("নেট", "MajorLogin রিকোয়েস্ট পাঠানো হচ্ছে ...")
        major_res = await send_majorlogin(client_http, payload, release_version, server_url)
        if not major_res or not major_res.account_uid:
            log("ত্রুটি", "MajorLogin সার্ভার দ্বারা প্রত্যাখ্যাত হয়েছে।")
            return None
        log("সফল", f"অ্যাকাউন্ট UID গৃহীত: {major_res.account_uid}")

        log("নেট", "GetLoginData রিকোয়েস্ট পাঠানো হচ্ছে ...")
        gl = await send_getlogin(client_http, payload, major_res.url, major_res.token, release_version)
        if not gl:
            log("ত্রুটি", "GetLoginData ব্যর্থ হয়েছে।")
            return None
        res_proto, dict_res = gl
        log("সফল", "লগইন তথ্য সফলভাবে গৃহীত হয়েছে।")

        online_addr = res_proto.Online_IP_Port or get_proto_field(dict_res, 14, "0.0.0.0:0")
        if ':' in online_addr:
            online_ip, online_port = online_addr.split(":")
        else:
            online_ip, online_port = "0.0.0.0", "0"

        chat_addr = res_proto.AccountIP_Port or get_proto_field(dict_res, 32, online_addr)
        if ':' in chat_addr:
            chat_ip, chat_port = chat_addr.split(":")
        else:
            chat_ip, chat_port = online_ip, online_port

        print_box("SAMI BD — লগইন সফল", [
            ("বট UID",      major_res.account_uid),
            ("অ্যাকাউন্ট নাম", res_proto.AccountName or "অজানা"),
            ("অঞ্চল",        major_res.region or region_pref),
            ("গিল্ড ID",     res_proto.Clan_ID or 0),
            ("অনলাইন",       f"{online_ip}:{online_port}"),
            ("চ্যাট",        f"{chat_ip}:{chat_port}"),
            ("সার্ভার",      major_res.url),
        ])

        return {
            "bot_uid":      str(major_res.account_uid),
            "token":        major_res.token,
            "region":       major_res.region or region_pref,
            "key":          major_res.key or AES_KEY,
            "iv":           major_res.iv or AES_IV,
            "timestamp":    major_res.timestamp or int(time.time()),
            "online_ip":    online_ip,
            "online_port":  online_port,
            "chat_ip":      chat_ip,
            "chat_port":    chat_port,
            "account_name": res_proto.AccountName or "অজানা",
            "clan_id":      res_proto.Clan_ID or 0,
            "clan_data":    res_proto.Clan_Compiled_Data or "",
            "server_url":   major_res.url,
        }


# ═══════════════════════════════════════════════════════════════
#              ★ সহায়ক ফাংশন ★
# ═══════════════════════════════════════════════════════════════

def get_random_color():
    colors = [
        "[FF0000]", "[00FF00]", "[0000FF]", "[FFFF00]", "[FF00FF]", "[00FFFF]", "[FFFFFF]", "[FFA500]",
        "[A52A2A]", "[800080]", "[000000]", "[808080]", "[C0C0C0]", "[FFC0CB]", "[FFD700]", "[ADD8E6]",
        "[90EE90]", "[D2691E]", "[DC143C]", "[00CED1]", "[9400D3]", "[F08080]", "[20B2AA]", "[FF1493]",
        "[7CFC00]", "[B22222]", "[FF4500]", "[DAA520]", "[00BFFF]", "[00FF7F]", "[4682B4]", "[6495ED]",
        "[5F9EA0]", "[DDA0DD]", "[E6E6FA]", "[B0C4DE]", "[556B2F]", "[8FBC8F]", "[2E8B57]", "[3CB371]",
        "[6B8E23]", "[808000]", "[B8860B]", "[CD5C5C]", "[8B0000]", "[FF6347]", "[FF8C00]", "[BDB76B]"
    ]
    return random.choice(colors)


def build_ob55_online_auth(account_uid, token, kts, key, iv):
    token_bytes = token.encode("utf-8")
    cipher = AES.new(key, AES.MODE_CBC, iv)
    enc_token = cipher.encrypt(pad(token_bytes, 16))
    opcode = bytes.fromhex("830c")
    uid_bytes = int(account_uid).to_bytes(8, byteorder="big")
    kts_bytes = int(kts).to_bytes(4, byteorder="big")
    len_bytes = len(enc_token).to_bytes(8, byteorder="big")
    return opcode + uid_bytes + kts_bytes + len_bytes + enc_token, enc_token


def create_auth_token_chat(account_id, jwt_token, timestamp, key, iv):
    try:
        K = bytes.fromhex(key) if isinstance(key, str) else key
        V = bytes.fromhex(iv) if isinstance(iv, str) else iv
        jwt_bytes = jwt_token.encode('utf-8')
        ct = AES.new(K, AES.MODE_CBC, V).encrypt(pad(jwt_bytes, AES.block_size))
        uid_b = int(account_id).to_bytes(8, 'big')
        ts_b = int(timestamp).to_bytes(4, 'big')
        len_b = len(ct).to_bytes(4, 'big')
        header = bytes.fromhex('6d19') + uid_b + ts_b + len_b
        return (header + ct).hex()
    except Exception as e:
        print_tag(f"অথেনটিকেশন টোকেন সমস্যা: {e}", "red")
        return None


async def cHTypE(H):
    if not H: return 'Squid'
    elif H == 1 or H == 3: return 'CLan'
    elif H == 2: return 'PrivaTe'
    return 'Squid'


async def DecodeWhisperMessage(hex_packet):
    packet = bytes.fromhex(hex_packet)
    proto = DEcwHisPErMsG_pb2.DecodeWhisper()
    proto.ParseFromString(packet)
    return proto


async def GeTSQDaTa(D):
    try:
        return D['5']['data']['1']['data'], D['5']['data']['17']['data'], D['5']['data']['31']['data']
    except KeyError:
        return None, None, None


async def get_colorful_message(message_text, message_number):
    color_palette = ["FF0000", "FFFF00", "0000FF", "FF00FF", "00FFFF", "FFA500",
                     "FF1493", "00FF7F", "7B68EE", "FF66CC", "00CED1", "FF69B4",
                     "32CD32", "9370DB", "FF4500", "1E90FF", "ADFF2F", "FF6347"]
    color_index = (message_number - 1) % len(color_palette)
    return f"[C][B][{color_palette[color_index]}]{message_text}"


# ═══════════════════════════════════════════════════════════════
#              ★ প্যাকেট বিল্ডার ★
# ═══════════════════════════════════════════════════════════════

async def SEndMsG(H, message, Uid, chat_id, key, iv):
    TypE = await cHTypE(H)
    if TypE == 'Squid': msg_packet = await xSEndMsgsQ(message, chat_id, key, iv, region or "BD")
    elif TypE == 'CLan': msg_packet = await xSEndMsg(message, 1, chat_id, chat_id, key, iv)
    elif TypE == 'PrivaTe': msg_packet = await xSEndMsg(message, 2, Uid, Uid, key, iv)
    return msg_packet


async def SEndPacKeT(OnLinE, ChaT, TypE, PacKeT):
    if TypE == 'ChaT' and ChaT: whisper_writer.write(PacKeT); await whisper_writer.drain()
    elif TypE == 'OnLine': online_writer.write(PacKeT); await online_writer.drain()
    else: return 'সমর্থিত নয়'


async def safe_send_message(chat_type, message, target_uid, chat_id, key, iv, max_retries=3):
    for attempt in range(max_retries):
        try:
            P = await SEndMsG(chat_type, message, target_uid, chat_id, key, iv)
            await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)
            return True
        except Exception:
            if attempt < max_retries - 1:
                await asyncio.sleep(0.5)
    return False


# ═══════════════════════════════════════════════════════════════
#      ★ DOT S1-S11 — ৯টি হ্যান্ডলার (main.py ডিসপ্যাচার) ★
# ═══════════════════════════════════════════════════════════════

async def handle_dot_s1(uid, chat_id, key, iv, region, chat_type, bot_uid):
    """`.S1` — ব্যাটল রয়্যাল গ্রুপ ইনভাইট"""
    try:
        bot_nick = globals().get('bot_nickname', 'SAMI BD')
        pkt = await S1_GroupInvitePacket(uid, chat_id, chat_type, key, iv, region, bot_uid, bot_nick)
        if pkt and whisper_writer:
            whisper_writer.write(pkt); await whisper_writer.drain()
            print_tag("✅ .S1 — ব্যাটল রয়্যাল ইনভাইট পাঠানো হয়েছে", "green")
            await safe_send_message(chat_type, "[B][C][00FF00]✅ .S1 — ব্যাটল রয়্যাল ইনভাইট পাঠানো হয়েছে!", uid, chat_id, key, iv)
            return True
        return False
    except Exception as e:
        print_tag(f"❌ .S1 ত্রুটি: {e}", "red")
        return False


async def handle_dot_s2(uid, chat_id, key, iv, region, chat_type, bot_uid):
    """`.S2` — BR র‍্যাংক ইনভাইট"""
    try:
        bot_nick = globals().get('bot_nickname', 'SAMI BD')
        pkt = await S2_BrRankInvitePacket(uid, chat_id, chat_type, key, iv, region, bot_uid, bot_nick)
        if pkt and whisper_writer:
            whisper_writer.write(pkt); await whisper_writer.drain()
            print_tag("✅ .S2 — BR র‍্যাংক ইনভাইট পাঠানো হয়েছে", "green")
            await safe_send_message(chat_type, "[B][C][00FF00]✅ .S2 — BR র‍্যাংক ইনভাইট পাঠানো হয়েছে!", uid, chat_id, key, iv)
            return True
        return False
    except Exception as e:
        print_tag(f"❌ .S2 ত্রুটি: {e}", "red")
        return False


async def handle_dot_s3(uid, chat_id, key, iv, region, chat_type, bot_uid):
    """`.S3` — রুম রিক্রুট"""
    try:
        bot_nick = globals().get('bot_nickname', 'SAMI BD')
        pkt = await S3_RoomRecruitPacket(uid, chat_id, chat_type, key, iv, region, bot_uid, bot_nick)
        if pkt and whisper_writer:
            whisper_writer.write(pkt); await whisper_writer.drain()
            print_tag("✅ .S3 — রুম রিক্রুট পাঠানো হয়েছে", "green")
            await safe_send_message(chat_type, "[B][C][00FF00]✅ .S3 — রুম রিক্রুট পাঠানো হয়েছে!", uid, chat_id, key, iv)
            return True
        return False
    except Exception as e:
        print_tag(f"❌ .S3 ত্রুটি: {e}", "red")
        return False


async def handle_dot_s4(uid, chat_id, key, iv, region, chat_type, bot_uid):
    """`.S4` — ইনভিজিবল রয়্যাল"""
    try:
        bot_nick = globals().get('bot_nickname', 'SAMI BD')
        pkt = await S4_InvisibleRoyalPacket(uid, chat_id, chat_type, key, iv, region, bot_uid, bot_nick)
        if pkt and whisper_writer:
            whisper_writer.write(pkt); await whisper_writer.drain()
            print_tag("✅ .S4 — ইনভিজিবল রয়্যাল পাঠানো হয়েছে", "green")
            await safe_send_message(chat_type, "[B][C][00FF00]✅ .S4 — ইনভিজিবল রয়্যাল পাঠানো হয়েছে!", uid, chat_id, key, iv)
            return True
        return False
    except Exception as e:
        print_tag(f"❌ .S4 ত্রুটি: {e}", "red")
        return False


async def handle_dot_s5(uid, chat_id, key, iv, region, chat_type, bot_uid):
    """`.S5` — গিল্ড ইনভাইট"""
    try:
        bot_nick = globals().get('bot_nickname', 'SAMI BD')
        pkt = await S5_GuildInvitePacket(uid, chat_id, chat_type, key, iv, region, bot_uid, bot_nick)
        if pkt and whisper_writer:
            whisper_writer.write(pkt); await whisper_writer.drain()
            print_tag("✅ .S5 — গিল্ড ইনভাইট পাঠানো হয়েছে", "green")
            await safe_send_message(chat_type, "[B][C][00FF00]✅ .S5 — গিল্ড ইনভাইট পাঠানো হয়েছে!", uid, chat_id, key, iv)
            return True
        return False
    except Exception as e:
        print_tag(f"❌ .S5 ত্রুটি: {e}", "red")
        return False


async def handle_dot_s6(uid, chat_id, key, iv, region, chat_type, bot_uid):
    """`.S6` — HUD শেয়ার"""
    try:
        bot_nick = globals().get('bot_nickname', 'SAMI BD')
        pkt = await S6_HudSharePacket(uid, chat_id, chat_type, key, iv, region, bot_uid, bot_nick)
        if pkt and whisper_writer:
            whisper_writer.write(pkt); await whisper_writer.drain()
            print_tag("✅ .S6 — HUD শেয়ার পাঠানো হয়েছে", "green")
            await safe_send_message(chat_type, "[B][C][00FF00]✅ .S6 — HUD শেয়ার পাঠানো হয়েছে!", uid, chat_id, key, iv)
            return True
        return False
    except Exception as e:
        print_tag(f"❌ .S6 ত্রুটি: {e}", "red")
        return False


async def handle_dot_s7(uid, chat_id, key, iv, region, chat_type, bot_uid):
    """`.S7` — ক্রাফটল্যান্ড ম্যাপ"""
    try:
        bot_nick = globals().get('bot_nickname', 'SAMI BD')
        pkt = await S7_CraftlandMapPacket(uid, chat_id, chat_type, key, iv, region, bot_uid, bot_nick)
        if pkt and whisper_writer:
            whisper_writer.write(pkt); await whisper_writer.drain()
            print_tag("✅ .S7 — ক্রাফটল্যান্ড ম্যাপ পাঠানো হয়েছে", "green")
            await safe_send_message(chat_type, "[B][C][00FF00]✅ .S7 — ক্রাফটল্যান্ড ম্যাপ পাঠানো হয়েছে!", uid, chat_id, key, iv)
            return True
        return False
    except Exception as e:
        print_tag(f"❌ .S7 ত্রুটি: {e}", "red")
        return False


async def handle_dot_s8(uid, chat_id, key, iv, region, chat_type, bot_uid):
    """`.S8` — ইনভিজিবল বাফ"""
    try:
        bot_nick = globals().get('bot_nickname', 'SAMI BD')
        pkt = await S8_InvisibleBuffPacket(uid, chat_id, chat_type, key, iv, region, bot_uid, bot_nick)
        if pkt and whisper_writer:
            whisper_writer.write(pkt); await whisper_writer.drain()
            print_tag("✅ .S8 — ইনভিজিবল বাফ পাঠানো হয়েছে", "green")
            await safe_send_message(chat_type, "[B][C][00FF00]✅ .S8 — ইনভিজিবল বাফ পাঠানো হয়েছে!", uid, chat_id, key, iv)
            return True
        return False
    except Exception as e:
        print_tag(f"❌ .S8 ত্রুটি: {e}", "red")
        return False


async def handle_dot_s11(uid, chat_id, key, iv, region, chat_type, bot_uid):
    """`.S11` — রিলে মার্ট ডিসকাউন্ট শেয়ার"""
    try:
        bot_nick = globals().get('bot_nickname', 'SAMI BD')
        pkt = await S11_DiscountSharePacket(uid, chat_id, chat_type, key, iv, region, bot_uid, bot_nick)
        if pkt and whisper_writer:
            whisper_writer.write(pkt); await whisper_writer.drain()
            print_tag("✅ .S11 — রিলে মার্ট ডিসকাউন্ট পাঠানো হয়েছে", "green")
            await safe_send_message(chat_type, "[B][C][00FF00]✅ .S11 — রিলে মার্ট ডিসকাউন্ট শেয়ার পাঠানো হয়েছে!", uid, chat_id, key, iv)
            return True
        return False
    except Exception as e:
        print_tag(f"❌ .S11 ত্রুটি: {e}", "red")
        return False


# ═══════════════════════════════════════════════════════════════
#              ★ স্কোয়াড / ইনভাইট / অ্যানিমেশন ★
# ═══════════════════════════════════════════════════════════════

async def Fixed_ChangeSquad(size, uid, K, V, region):
    fields = {
        1: 17,
        2: {1: int(uid), 2: 1, 3: int(size-1), 4: 62, 5: "\u001a", 8: 5, 13: 329}
    }
    if region.lower() == "ind": packet = '0514'
    elif region.lower() == "bd": packet = "0519"
    else: packet = "0515"
    return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex(), packet, K, V)


async def Fixed_SendInvite(size, target_uid, K, V, region):
    fields = {
        1: 2,
        2: {1: int(target_uid), 2: region.upper(), 4: int(size)}
    }
    if region.lower() == "ind": packet = '0514'
    elif region.lower() == "bd": packet = "0519"
    else: packet = "0515"
    return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex(), packet, K, V)


async def JoinSq_original(code, K, V):
    skinz = {1: 4, 2: {4: r"\u0001\u0007\t\n\u000b\u0012\u0019 '", 5: str(code), 6: 6, 8: 1,
        9: {1: "08FFF3BE903F27DF0203110111110000006B0003006800169194106F13CF106E4676251411010404dfe9e8b5ca3ca4f96a3119c00000004f03060301cacfa16d",
            2: 130, 3: r"tY_S\u0013\b\u0001M\u0002\u0000T\u0000\u0005\u000e\b\t\u0002\u0000\u0003U\u0003\u0001V\u000fR\u000e\tRQ\u0002\u0004\u0005US\u0003XS\u0005\u0001\u0002\u0011\u0001\u0002JuTAEN\u001e\u0002\u001c\u0002\u001f\u0013\b\u0003M\u001cDbz_Q@}p_QOgsC\u001dYVI\u0004UAAj_ga\u0004\u0012\u0000K\u001d\u0007_t\u0019b\bCx\u0002UeGat\u001fTTCBLER`\u0006\u0001\r\f\u0012\u0006\u0005N^^\u0002acH~r\u0004_\u0003RO|\u000bcd_@~`Rnqrgh\n\u0015\nL\\Nh\u0000~G\u000et\u0000eb]VQ\u0006t^F[ZIGxCdZD\u000b\u0011\u0002OA~LP@\u000fcSDyATQApaT^{|wa]\\\u0001E\u000f\u0013\nJfxve}\u0004J\u0003c{YL\u0007^^yDYQf\bhe\u0005_wg\r\u0010\u0007\bEHpX@||\u0002Z\\uTGyA\u0001JP\u0005t~VkTE\u0000J\\\u000b\u0013\nMr\u0018zTzK}qE]vnvwROuheYvwduvQ\r\u001a\u0005M\u0006z\u001dfXfzvHFc~dXUz}O\u001aB\u0005t\u0002i\u001co_\u0004\u0012\u0003\u0007J\u0006b\u0003\u000eqlfvbEstgu~wB\u0001v@`yI\u0002ZPx\f\u0014\u0003NR\u0002yBZvuD_cd\u0004q]lH]\u0007bD}pCe\t\u0004t\n",
            4: "w^_R", 6: 11, 7: r"\u0014\u0004aqrg\u0015\u0013", 8: "1.132.1", 9: 3, 10: 2,
            11: "\u0003bbSQ6wxegh9qAdV2KyoVleA17yPmYF+yTnOrl+JMknmppeUBe5ZsiHueP2mZZ4KOs6b2Ail1S9z3qIeU9hGFZ2M6PP39/zjIc/RFVPAkgDagySswMVmYaPhkzU5IqNPow2843fyQUz9xI10NdMhl1WiI4Y6wCXBotiUS9wSgujQ4j0fWXUyklCxBWo8r27hyoGSVrPdTPXFMnJJpPRRFFmWqc3fWvMg+BNfxSRJOZRSrkzG0nNvSIJ4uZB2pqAlHIPEYx7bI6zsgwUVDiLZJKTUTyuCGbOd1DegDUFfazFesTG1LJknT5WhgzCsrBIy+f2l+LeJe5DW7wEwNaHambM7ECXcJcLIhB9kJJsW0tFvXkk3HSdcQ8N1K6wjSKWhpkW0kV8Zrjj0jkhS/7AZ6T9GJRIA827YDtTorBvbx1UkXjYrqYI1nSa2GaMexGnqlurc5DE3v1R+mUBI9GqmjEPgTSYVBxyeCdQMHaMXGtspAhvkiO84ToU87sP45pylDEfFOVoc/rcmdzWeqlYPsv6txKRtIHcb0cO+MoVShoU8ZUVRDF3znbqzVrscPIfplBaa79lwvQqzRubLl9XY="},
        11: {1: "IDC4", 2: 281, 3: "ME"}, 13: "fr", 16: "7OR\u0019", 20: r"\b\u0015", 27: r"\bH\u0010\u0003"}}
    return await GeneRaTePk((await CrEaTe_ProTo(skinz)).hex(), '0515', K, V)


async def MahirAccepted(uid, code, K, V, region):
    fields = {1: 4, 2: {1: int(uid), 3: int(uid), 4: r"rYUW\u0017\t\u0007NR\u000f\u0005\u0004\\W\u0002\u000fV\u0004TPQ\u0003\u000f\u0005\u0004]\u0005\u000b\u0000\u0002W\u0005\r\nVY\u0004\u0007\u0007\u0007\u0017\u0001\bNQ\fS\u0005\u000e\u0006\f\u0005\rT\u0002\r\u0000TS\u0007U\u0004X\u0006RY\u0005\u0003\u0003SW\u0000\u000eQ\u0000^\u0014\u0003\u0004JXS\u000f\u0000g{gqfePblEZJp{_xU\bmQW\f\u0007\u000f\u0015\u0007H\\U^CHXh@Ax`\u000f~\rPN~Nz\\\u001fr_ckPU\u000b\u0015\u0005\u0003Ekfp\u07fcY\u0001nWV\u0002\u0005azE~N\u0007HTg\u0007w}@\u0002{\t\u0013\u0001NeNP]DUf|]ugINs{\u0001\\rAgB_\u0004fA]\u0004\r\u001a\u0000HpOv\\\u0005|gS\u0019\\A\u07fWW\u0003\u07fTqFGi\u0004Qr\u0019dW\u0004\u0011\rD\u0002yeZ]A\u0016a\u0007Ungeg\u0007E\\P\u001b\u000b\u0004\u0005dd\ff\r\u000f\u0017\t\u000fNRyZd\u0012tZ\fe\u0007AGv\u07fw]{P\u001c\u07f\u000ff\u0005ZJK\u0004\u0005\u0014\u0001Jgq\u001frymsB\u0001\u000fd`\u001bj~[}\u0004SDZ|IxKB\u0000\n\u0011\u0002J^`tjYN\u0007WQdE[PQ\u0002_{VP`S\t\u07f\u001dP\n\u000f\u000f\u0015\u0004\u0004L{V\u0003@yP[rgJ{Hpk\u0001\u000bw\u0001Agt_\u0003HxPc\u000b\u0017\u0005E`y\ngWoy\u0006S{A\u001b``Y\u0002Xzw}dDWOKsg\t\u0013\u000eNf\u000e\\`\u0005AwJc\u0003BM\u0001^\u0000R\u0002Qoh]tbS~`G\r\u001a\u0004HibAQ\u000f^XNt~kDUWaeaNqcLQ]Py[G\u0004",
            8: 1, 9: {1: "08FBA33CFF105FDD02030A01111100000003000100020000B687046B0D6D2083467625141101030175a63c900e748c3f6a311e04000000ff00040202cacfa16d",
            2: 197, 3: "735154531406054a035305025a0e50560f5100040250020f5e0401520653000303505e0d520302501500064d705548424e1f051a001e12040a441d45677f5a56477574565e4f6274451d585849005a4f456d5b64670c1400496d017842740c670100040069536e72586c02016e657e566b524403081500044d0d515b637f757c19095c7c510b00417f565e5e066f5b584d6e02400a160e4d58496d0177400e750763605c575d0f7d5f475e5f4c407f4b60534b0b140549751e66407a4860726e44400e6103557e515c646f43577106077b60051b0f4b4e474e58457e4f615c01406000051e0361516e7b67614e040102540c1609004a0e40730f62517f446a135179507e706850547f7e7a67795553597c0a1206445b456640046265725c4d505d446d50737b7c42035970486370645e0b12034d506f5c7a1c554f574b0e765a0f0a7364505203477569456c6c420f0a1604014b647149136c186f795f5d78755e550e7842545e53747b08705f7f5d0a14004a08666b5a5b5f00045c7f5e584d72584262705f56055c61475564790515004b76514178587f52797a0f077a070953507d7f4d784f794f667b4256081b0e4a75627d4778417a06717574747c4c78557b4b7a0a697f0e714573600a",
            4: "{Y_R", 6: 13, 7: "1c6f017306741513", 8: "2.126.22", 9: 2, 10: 1,
            11: "036262535136784d584e38742b416456324b796f566c6537392f763672324d4773683377706379634f6b6b6f7447397934523930517432797246474c464c624c777a7747344d4d5257623146756d2b6556777a62597736743973492b787059612f55596e43465a59485235713348705830306c485a6f3632565145574e7145705866414c38734a754646575247386d376f5444566a4c484c576e714c52576f4e653236437a734c346a4144482b71694b55384d71476c5936546669544863716c487a345568463869396a365233366d49774b71746c36714f797568513854367945714b69742f45466d2b3636634b787649304f384d6c41385166454b6253467366477a2f30684e6a543873305369722f3962635a2f4679376c752f61632f366765704d415734566b442b36374f535756473665377a775a79312b797a42334b70632b7571782b577437414d39727761644439575765704570567849526d66654f5847627775787a68574b5664344c49586f415a364b387063647450627953575857455135706a542b653669365a2f6177444a3179356f774d5a534f64487262392b7877424a4d444f7848565a7a483372547a30314a316738517675466b656c3042433746473630683456427041494457487956684e794b4f5145507139467a4a6272686b316146306768766578512f6a2f484767426a5268675134645243372b477a5a687a2b77505967376454746f2b494d56363774642b54435653314234346b4148395a6d415872763758615941626477644e664f533170484875736b7336346f72463452534d3772656345417661484e61484854314c5545686e786a5a616d4d4f303d"},
            10: str(code), 11: {1: "IDC3", 2: 84, 3: "BD"}, 13: "en", 16: "374f5219",
            20: {1: 21}, 23: "a_1477547277882450725", 27: {1: 2, 2: 8}}}
    return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex(), '0515', K, V)


async def leave_channel_req(channel_id, channel_type, key, iv):
    fields = {1: 4, 2: {1: int(channel_id), 2: int(channel_type), 3: "en"}}
    return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex(), '1215', key, iv)


async def animation_packet(animation_id, key, iv):
    fields = {1: 88, 2: {1: {1: int(animation_id)}}}
    packet_hex = (await CrEaTe_ProTo(fields)).hex()
    encrypted = await encrypt_packet(packet_hex, key, iv)
    pl = len(encrypted) // 2
    hl = format(pl, 'x')
    final = "051500" + "0" * (6 - len(hl)) + hl + encrypted
    return bytes.fromhex(final)


async def Look_Changer(bundle_id, key, iv, look_type=1, region="bd"):
    fields = {1: 88, 2: {1: {1: bundle_id, 2: look_type}, 2: 2}}
    packet_hex = (await CrEaTe_ProTo(fields)).hex()
    encrypted = await encrypt_packet(packet_hex, key, iv)
    hl = await DecodE_HeX(len(encrypted) // 2)
    if region.lower() == "ind": pt = "0514"
    elif region.lower() == "bd": pt = "0519"
    else: pt = "0515"
    if len(hl) == 2: h = f"{pt}000000"
    elif len(hl) == 3: h = f"{pt}00000"
    elif len(hl) == 4: h = f"{pt}0000"
    elif len(hl) == 5: h = f"{pt}000"
    else: h = f"{pt}000000"
    return bytes.fromhex(h + hl + encrypted)


# ═══════════════════════════════════════════════════════════════
#              ★ ব্যাজ প্যাকেট ও হ্যান্ডলার ★
# ═══════════════════════════════════════════════════════════════
async def request_join_with_badge(target_uid, badge_value, key, iv, region="IND"):
    try:
        avatar_id = int(await xBunnEr())
        fields = {
            1: 33,
            2: {
                1: int(target_uid), 2: region.upper(), 3: 1, 4: 1,
                5: bytes([1, 7, 9, 10, 11, 18, 25, 26, 32]),
                6: "SAMI BD", 7: 330, 8: 1000, 10: region.upper(),
                11: bytes([49,97,99,52,98,56,48,101,99,102,48,52,55,56,
                          97,52,52,50,48,51,98,102,56,102,97,99,54,49,
                          50,48,102,53]),
                12: 1, 13: int(target_uid),
                14: {
                    1: 2203434355, 2: 8,
                    3: b"\x10\x15\x08\x0A\x0B\x13\x0C\x0F\x11\x04\x07\x02\x03\x0D\x0E\x12\x01\x05\x06"
                },
                16: 1, 17: 1, 18: 312, 19: 46,
                23: bytes([16, 1, 24, 1]), 24: avatar_id, 26: {},
                27: {1: 11, 2: int(bot_uid) if bot_uid else 12999994075, 3: 9999},
                28: {}, 31: {1: 1, 2: int(badge_value)}, 32: int(badge_value),
                34: {
                    1: int(target_uid), 2: 8,
                    3: b"\x0F\x06\x15\x08\x0A\x0B\x13\x0C\x11\x04\x0E\x14\x07\x02\x01\x05\x10\x03\x0D\x12"
                }
            },
            10: "en",
            13: {2: 1, 3: 1}
        }
        proto_hex = (await CrEaTe_ProTo(fields)).hex()
        if region.lower() == "ind": pt = "0514"
        elif region.lower() == "bd": pt = "0519"
        else: pt = "0515"
        return await GeneRaTePk(proto_hex, pt, key, iv)
    except Exception as e:
        print_tag(f"ব্যাজ প্যাকেট ত্রুটি: {e}", "red")
        return None


async def handle_badge_command(cmd, inPuTMsG, uid, chat_id, key, iv, region, chat_type):
    parts = inPuTMsG.strip().split()
    badge_name = {
        "s1": "ক্রাফটল্যান্ড", "s2": "নিউ V", "s3": "মডারেটর",
        "s4": "ছোট V", "s5": "প্রো ব্যাজ",
    }.get(cmd, "ব্যাজ")

    if len(parts) < 2:
        msg = (
            f"[B][C][FFD700]✦ SAMI BD ✦\n"
            f"[B][C][FFFFFF]{badge_name}\n"
            f"[B][C][00FFFF]/{cmd} <uid>"
        )
        await safe_send_message(chat_type, msg, uid, chat_id, key, iv)
        return

    target_uid = parts[1].strip()
    if not target_uid.isdigit():
        msg = f"[B][C][FF0000]✦ SAMI BD ✦\n[B][C][FFFFFF]❌ শুধু সংখ্যা দাও"
        await safe_send_message(chat_type, msg, uid, chat_id, key, iv)
        return

    badge_value = BADGE_VALUES.get(cmd, 1048576)

    proc = (
        f"[B][C][00FFFF]✦ SAMI BD ✦\n"
        f"[B][C][FFFFFF]⏳ {badge_name}\n"
        f"[B][C][FFFFFF]🎯 {target_uid}"
    )
    await safe_send_message(chat_type, proc, uid, chat_id, key, iv)

    try:
        pkt = await request_join_with_badge(target_uid, badge_value, key, iv, region)
        if pkt:
            for i in range(5):
                await SEndPacKeT(whisper_writer, online_writer, 'OnLine', pkt)
                await asyncio.sleep(0.2)
            ok = (
                f"[B][C][00FF00]✦ SAMI BD ✦\n"
                f"[B][C][FFFFFF]✅ {badge_name}\n"
                f"[B][C][FFFFFF]🎯 {target_uid}\n"
                f"[B][C][FFFFFF]📤 ৫ বার"
            )
            await safe_send_message(chat_type, ok, uid, chat_id, key, iv)
        else:
            fail = f"[B][C][FF0000]✦ SAMI BD ✦\n[B][C][FFFFFF]❌ প্যাকেট ব্যর্থ"
            await safe_send_message(chat_type, fail, uid, chat_id, key, iv)
    except Exception as e:
        err = f"[B][C][FF0000]✦ SAMI BD ✦\n[B][C][FFFFFF]❌ {str(e)[:20]}"
        await safe_send_message(chat_type, err, uid, chat_id, key, iv)


# ═══════════════════════════════════════════════════════════════
#              ★ API কল ★
# ═══════════════════════════════════════════════════════════════

async def send_friend_request(target_uid, token, region):
    try:
        encrypted_id = Encrypt_ID(target_uid)
        payload = f"08a7c4839f1e10{encrypted_id}1801"
        kb = bytes([89, 103, 38, 116, 99, 37, 68, 69, 117, 104, 54, 37, 90, 99, 94, 56])
        ib = bytes([54, 111, 121, 90, 68, 114, 50, 50, 69, 51, 121, 99, 104, 106, 77, 37])
        cipher = AES.new(kb, AES.MODE_CBC, ib)
        ep = cipher.encrypt(pad(bytes.fromhex(payload), AES.block_size)).hex()
        url = "https://clientbp.ggpolarbear.com/RequestAddingFriend"
        headers = {"Authorization": f"Bearer {token}", "X-Unity-Version": "2018.4.11f1",
            "X-GA": "v1 1", "ReleaseVersion": "OB55",
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "Dalvik/2.1.0 (Linux; Android 9)"}
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, data=bytes.fromhex(ep), ssl=False) as r:
                return (True, "✅ ফ্রেন্ড রিকোয়েস্ট পাঠানো হয়েছে") if r.status == 200 else (False, f"❌ স্টেটাস: {r.status}")
    except Exception as e:
        return False, f"❌ ত্রুটি: {str(e)}"


async def remove_friend(target_uid, token, region):
    try:
        import RemoveFriend_Req_pb2
        msg = RemoveFriend_Req_pb2.RemoveFriend()
        msg.AuthorUid = int(admin_uid); msg.TargetUid = int(target_uid)
        kb = bytes([89, 103, 38, 116, 99, 37, 68, 69, 117, 104, 54, 37, 90, 99, 94, 56])
        ib = bytes([54, 111, 121, 90, 68, 114, 50, 50, 69, 51, 121, 99, 104, 106, 77, 37])
        cipher = AES.new(kb, AES.MODE_CBC, ib)
        eb = cipher.encrypt(pad(msg.SerializeToString(), AES.block_size))
        url = "https://clientbp.ggpolarbear.com/RemoveFriend"
        headers = {'Authorization': f"Bearer {token}", 'User-Agent': "Dalvik/2.1.0 (Linux; Android 9)",
            'Content-Type': "application/x-www-form-urlencoded", 'X-Unity-Version': "2018.4.11f1",
            'X-GA': "v1 1", 'ReleaseVersion': "OB55"}
        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=eb, headers=headers, ssl=False) as r:
                return (True, "✅ ফ্রেন্ড রিমুভ করা হয়েছে") if r.status == 200 else (False, f"❌ স্টেটাস: {r.status}")
    except Exception as e:
        return False, f"❌ ত্রুটি: {str(e)}"


async def check_banned(player_id):
    try:
        url = f"https://ff.garena.com/api/antihack/check_banned?lang=en&uid={player_id}"
        headers = {"User-Agent": "Mozilla/5.0 (Linux; Android 10)", "Accept": "application/json",
            "referer": "https://ff.garena.com/en/support/",
            "x-requested-with": "B6FksShzIgjfrYImLpTsadjS86sddhFH"}
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, ssl=False) as r:
                if r.status == 200:
                    return True, await r.json()
                return False, f"ব্যর্থ: {r.status}"
    except Exception as e:
        return False, f"ত্রুটি: {str(e)}"


async def get_player_info(player_id):
    try:
        url = f"https://nirob-x-info.vercel.app/info?uid={player_id}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url, ssl=False) as r:
                if r.status == 200:
                    return True, await r.json()
                return False, f"ব্যর্থ: {r.status}"
    except Exception as e:
        return False, f"ত্রুটি: {str(e)}"


def format_player_info(data):
    basic = data.get("basicInfo", {}); clan = data.get("clanBasicInfo", {})
    captain = data.get("captainBasicInfo", {}); pet = data.get("petInfo", {})
    social = data.get("socialInfo", {}); credit = data.get("creditScoreInfo", {})
    diamond = data.get("diamondCostRes", {})
    def x(v): return str(v) if v else "0"
    m1 = f"[b][c]{get_random_color()} 🎮 প্লেয়ার তথ্য\n[b][c][FFFFFF]নাম: {captain.get('nickname', basic.get('nickname', 'অজানা'))}\n[b][c][FFFFFF]ইউআইডি: {x(captain.get('accountId', basic.get('accountId', '0')))}\n[b][c][FFFFFF]লাইক: {x(captain.get('liked', basic.get('liked', '0')))}\n[b][c][FFFFFF]লেভেল: {captain.get('level', basic.get('level', '0'))}\n[b][c][FFFFFF]অঞ্চল: {captain.get('region', basic.get('region', 'অজানা'))}"
    m2 = f"[b][c]{get_random_color()} 🏰 গিল্ড তথ্য\n[b][c][FFFFFF]গিল্ড: {clan.get('clanName', 'কোন গিল্ড নেই')}\n[b][c][FFFFFF]গিল্ড আইডি: {x(clan.get('clanId', '0'))}\n[b][c][FFFFFF]লিডার: {x(clan.get('captainId', 'অজানা'))}\n[b][c][FFFFFF]সদস্য: {clan.get('memberNum', '0')}/{clan.get('capacity', '0')}\n[b][c][FFFFFF]লেভেল: {clan.get('clanLevel', '0')}"
    m3 = f"[b][c]{get_random_color()} ℹ️ অতিরিক্ত তথ্য\n[b][c][FFFFFF]পেট: {pet.get('name', 'N/A')} (লেভেল {pet.get('level', 'N/A')})\n[b][c][FFFFFF]ক্রেডিট: {credit.get('creditScore', 'N/A')}\n[b][c][FFFFFF]ডায়মন্ড: {diamond.get('diamondCost', 'N/A')}\n[b][c][FFFFFF]বায়ো: {social.get('signature', 'N/A')}"
    return m1, m2, m3


def format_check_result(data):
    try:
        return f"[b][c]{get_random_color()} 🔍 ব্যান চেক\n[b][c][FFFFFF]ধরন: {data.get('ban_type', 'অজানা')}\n[b][c][FFFFFF]সময়কাল: {data.get('ban_duration', 'অজানা')}"
    except Exception as e:
        return f"[b][c]ত্রুটি: {str(e)}"


# ═══════════════════════════════════════════════════════════════
#              ★ ইভো সাইকেল লুপ ★
# ═══════════════════════════════════════════════════════════════

async def evo_gun_cycle(uids, evo_ids_list, key, iv, region):
    global evo_cycle_running
    while evo_cycle_running:
        for emote_id in evo_ids_list:
            if not evo_cycle_running: break
            for uid_str in uids:
                try:
                    H = await Emote_k(int(uid_str), int(emote_id), key, iv, region)
                    await SEndPacKeT(whisper_writer, online_writer, 'OnLine', H)
                except Exception:
                    pass
            if evo_cycle_running:
                for i in range(5):
                    if not evo_cycle_running: break
                    await asyncio.sleep(1)
        if evo_cycle_running:
            await asyncio.sleep(2)


# ═══════════════════════════════════════════════════════════════
#              ★ ইনভাইট স্বাগতম বার্তা ★
# ═══════════════════════════════════════════════════════════════

WELCOME_DELAY = 3
_welcomed = {}

async def send_welcome(chat_code, key, iv):
    try:
        now = time.time()
        if now - _welcomed.get(chat_code, 0) < 60:
            return
        _welcomed[chat_code] = now
        await asyncio.sleep(WELCOME_DELAY)
        msg = (
            "[B][C][B][C][FFD700]আসসালামু আলাইকুম।\n"
            "[B][C][FF00FF]SAMI BD বটে আপনাকে স্বাগতম।\n"
            "[B][C][00FFFF]আশা করি, বটটি ব্যবহার করে ভালো লাগবে।"
        )
        await safe_send_message(0, msg, None, chat_code, key, iv)
    except Exception:
        pass


# ═══════════════════════════════════════════════════════════════
#              ★ TCP অনলাইন হ্যান্ডলার ★
# ═══════════════════════════════════════════════════════════════

async def TcPOnLine(ip, port, key, iv, AutHToKen, reconnect_delay=0.5):
    global online_writer, whisper_writer, region, bot_uid
    while True:
        try:
            reader, writer = await asyncio.open_connection(ip, int(port))
            online_writer = writer
            token_bytes = bytes.fromhex(AutHToKen) if isinstance(AutHToKen, str) else AutHToKen
            writer.write(token_bytes); await writer.drain()
            print_tag(f"অনলাইন সার্ভারে সংযুক্ত: {ip}:{port}", "green")
            while True:
                data = await reader.read(9999)
                if not data: break
                hex_data = data.hex()
                if not hex_data.startswith("0500"): continue
                try: packet_json = json.loads(await DeCode_PackEt(hex_data[10:]))
                except Exception: continue

                try:
                    if ('5' in packet_json and 'data' in packet_json['5'] and '1' in packet_json['5']['data'] and '8' in packet_json['5']['data']):
                        owner = packet_json['5']['data']['1']['data']
                        code = packet_json['5']['data']['8']['data']
                        print_tag(f"স্কোয়াড ইনভাইট: {owner}", "yellow")
                        join_pkt = await MahirAccepted(owner, code, key, iv, region)
                        if join_pkt and online_writer:
                            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', join_pkt)
                except Exception:
                    pass

                try:
                    uid_g, chat_code, squad_code = await GeTSQDaTa(packet_json)
                    if uid_g is not None:
                        INV_JOIN = await AutH_Chat(3, uid_g, chat_code, key, iv)
                        await SEndPacKeT(whisper_writer, online_writer, 'ChaT', INV_JOIN)
                        asyncio.create_task(send_welcome(uid_g, key, iv))
                except Exception:
                    pass

                try:
                    if packet_json.get('4', {}).get('data') == 8:
                        f5 = packet_json.get('5', {}).get('data', {})
                        if f5.get('2', {}).get('data') == 5:
                            chat_code = f5.get('17', {}).get('data')
                            if chat_code is not None:
                                LeAvE = await leave_channel_req(chat_code, 3, key, iv)
                                await SEndPacKeT(whisper_writer, online_writer, 'ChaT', LeAvE)
                                print_tag("কিক হয়েছে! চ্যানেল ছেড়ে যাওয়া হয়েছে", "red")
                except Exception:
                    pass
            writer.close(); await writer.wait_closed(); online_writer = None
        except Exception as e:
            print_tag(f"অনলাইন সার্ভার সমস্যা: {ip}:{port} - {e}", "red")
            online_writer = None
        await asyncio.sleep(reconnect_delay)


# ═══════════════════════════════════════════════════════════════
#              ★ TCP চ্যাট হ্যান্ডলার ★
# ═══════════════════════════════════════════════════════════════

async def TcPChaT(ip, port, AutHToKen, key, iv, login_data, ready_event, region, reconnect_delay=0.5):
    global whisper_writer, online_writer, ToKen, bot_uid, bot_enabled
    global bot_nickname, bot_clan_id
    global evo_cycle_running, evo_cycle_task

    print_tag(f"{region} → চ্যাট সার্ভারে সংযুক্ত হচ্ছে...", "cyan")
    while True:
        try:
            reader, writer = await asyncio.open_connection(ip, int(port))
            whisper_writer = writer
            bytes_payload = bytes.fromhex(AutHToKen) if isinstance(AutHToKen, str) else AutHToKen
            whisper_writer.write(bytes_payload); await whisper_writer.drain()
            ready_event.set()
            print_tag(f"চ্যাট সার্ভারে সংযুক্ত: {ip}:{port}", "green")

            clan_id = login_data.get("clan_id", 0)
            clan_data = login_data.get("clan_data", "")
            if clan_id:
                try:
                    pK = await AuthClan(int(clan_id), str(clan_data), key, iv)
                    if whisper_writer:
                        whisper_writer.write(pK)
                        await whisper_writer.drain()
                        print_tag(f"গিল্ড অথেনটিকেশন সফল! গিল্ড আইডি: {clan_id}", "green")
                except Exception as e:
                    print_tag(f"গিল্ড অথেনটিকেশন ব্যর্থ: {e}", "red")

            while True:
                data = await reader.read(9999)
                if not data: break
                if not data.hex().startswith("120000"): continue
                try:
                    response = await DecodeWhisperMessage(data.hex()[10:])
                    uid = response.Data.uid
                    chat_id = response.Data.Chat_ID
                    XX = response.Data.chat_type
                    inPuTMsG = response.Data.msg.lower()
                    msg_raw = response.Data.msg
                except Exception:
                    continue

                # ═══════════════════════════════════════════════
                # .S1 / .S2 / .S3 / .S4 / .S5 / .S6 / .S7 / .S8 / .S11
                # ═══════════════════════════════════════════════
                _cmd = msg_raw.strip()
                if _cmd == '.S1':
                    await handle_dot_s1(uid, chat_id, key, iv, region, XX, bot_uid)
                    continue
                elif _cmd == '.S2':
                    await handle_dot_s2(uid, chat_id, key, iv, region, XX, bot_uid)
                    continue
                elif _cmd == '.S3':
                    await handle_dot_s3(uid, chat_id, key, iv, region, XX, bot_uid)
                    continue
                elif _cmd == '.S4':
                    await handle_dot_s4(uid, chat_id, key, iv, region, XX, bot_uid)
                    continue
                elif _cmd == '.S5':
                    await handle_dot_s5(uid, chat_id, key, iv, region, XX, bot_uid)
                    continue
                elif _cmd == '.S6':
                    await handle_dot_s6(uid, chat_id, key, iv, region, XX, bot_uid)
                    continue
                elif _cmd == '.S7':
                    await handle_dot_s7(uid, chat_id, key, iv, region, XX, bot_uid)
                    continue
                elif _cmd == '.S8':
                    await handle_dot_s8(uid, chat_id, key, iv, region, XX, bot_uid)
                    continue
                elif _cmd == '.S11':
                    await handle_dot_s11(uid, chat_id, key, iv, region, XX, bot_uid)
                    continue

                if not bot_enabled and not inPuTMsG.strip().startswith('/on'):
                    if inPuTMsG.strip() != '/on': continue

                # ═══════════════════════════════════════════════
                # সাহায্য
                # ═══════════════════════════════════════════════
                if inPuTMsG.strip() in ("/help", "help", "bot help"):
                    box1 = """
[B][C][00FFFF]╭━━━━━━━━━━━━━━━━━━━━╮
[B][C][FFD700]      ✦ SAMI BD ✦
[B][C][00FF7F]       HELP CENTER
[B][C][00FFFF]╰━━━━━━━━━━━━━━━━━━━━╯
[B][C][FF00FF]◆ [00FF7F]SQUAD JOIN
[B][C][00FFFF]   └── /join <txt>
[B][C][FFD700]◇ 02 ┃ [00FF7F]SQUAD EXIT
[B][C][00FFFF]   └── /exit
[B][C][FF00FF]◆ 03 ┃ [00FF7F]3 PLAYER GROUP
[B][C][00FFFF]   └── /3
[B][C][FFD700]◇ 04 ┃ [00FF7F]5 PLAYER GROUP
[B][C][00FFFF]   └── /5
[B][C][FF00FF]◆ 05 ┃ [00FF7F]6 PLAYER GROUP
[B][C][00FFFF]   └── /6
[B][C][FFD700]═══════════════"""
                    await safe_send_message(XX, box1, uid, chat_id, key, iv)
                    await asyncio.sleep(0.5)

                    box2 = """
[B][C][00FFFF]╭━━━━━━━━━━━━━━━━━━━━╮
[B][C][FFD700]      ✦ SAMI BD ✦
[B][C][00FF7F]       HELP CENTER
[B][C][00FFFF]╰━━━━━━━━━━━━━━━━━━━━╯
[B][C][FF00FF]◆ [00FF7F]EVO EMOTE
[B][C][00FFFF]   └── /evo <UID> <NUMBER>
[B][C][FFD700]◇ 02 ┃ [00FF7F]EVO CYCLE
[B][C][00FFFF]   └── /evos
[B][C][FF00FF]◆ 03 ┃ [00FF7F]STOP CYCLE
[B][C][00FFFF]   └── /sevos
[B][C][FFD700]◇ 04 ┃ [00FF7F]SEND BUNDLE
[B][C][00FFFF]   └── /b <1-12>
[B][C][FF00FF]◆ 05 ┃ [00FF7F]EMOTE BY NAME
[B][C][00FFFF]   └── /e <NAME>
[B][C][FFD700]═══════════════"""
                    await safe_send_message(XX, box2, uid, chat_id, key, iv)
                    await asyncio.sleep(0.5)

                    box3 = """
[B][C][00FFFF]╭━━━━━━━━━━━━━━━━━━━━╮
[B][C][FFD700]      ✦ SAMI BD ✦
[B][C][00FF7F]       HELP CENTER
[B][C][00FFFF]╰━━━━━━━━━━━━━━━━━━━━╯
[B][C][FF00FF]◆ [00FF7F]EMOTE BY NUMBER
[B][C][00FFFF]   └── /e <NUMBER>
[B][C][FFD700]◇ 02 ┃ [00FF7F]LOVE MESSAGE
[B][C][00FFFF]   └── /love <NAME>
[B][C][FF00FF]◆ 03 ┃ [00FF7F]INSULT
[B][C][00FFFF]   └── /gali <NAME>
[B][C][FFD700]◇ 04 ┃ [00FF7F]ROAST
[B][C][00FFFF]   └── /rt <NAME>
[B][C][FF00FF]◆ 05 ┃ [00FF7F]COMPLIMENT
[B][C][00FFFF]   └── /praisa <NAME>
[B][C][FFD700]◇ 06 ┃ [00FF7F]S5 PRO BADGE
[B][C][00FFFF]   └── /s5 <UID>
[B][C][FFD700]═══════════════"""
                    await safe_send_message(XX, box3, uid, chat_id, key, iv)
                    await asyncio.sleep(0.5)

                    box4 = """
[B][C][00FFFF]╭━━━━━━━━━━━━━━━━━━━━╮
[B][C][FFD700]      ✦ SAMI BD ✦
[B][C][00FF7F]       HELP CENTER
[B][C][00FFFF]╰━━━━━━━━━━━━━━━━━━━━╯
[B][C][FF00FF]◆ [00FF7F]LOVE LETTER
[B][C][00FFFF]   └── /later <NAME>
[B][C][FFD700]◇ 02 ┃ [00FF7F]LUCK
[B][C][00FFFF]   └── /luck <NAME>
[B][C][FF00FF]◆ 03 ┃ [00FF7F]JOKES
[B][C][00FFFF]   └── /joke
[B][C][FFD700]◇ 04 ┃ [00FF7F]QUIZ
[B][C][00FFFF]   └── /quiz
[B][C][FF00FF]◆ 05 ┃ [00FF7F]DICE ROLL
[B][C][00FFFF]   └── /roll
[B][C][FFD700]═══════════════"""
                    await safe_send_message(XX, box4, uid, chat_id, key, iv)
                    await asyncio.sleep(0.5)

                    box5 = """
[B][C][00FFFF]╭━━━━━━━━━━━━━━━━━━━━╮
[B][C][FFD700]      ✦ SAMI BD ✦
[B][C][00FF7F]       HELP CENTER
[B][C][00FFFF]╰━━━━━━━━━━━━━━━━━━━━╯
[B][C][FF00FF]◆ [00FF7F]HOROSCOPE
[B][C][00FFFF]   └── /zodiac
[B][C][FFD700]◇ 02 ┃ [00FF7F]WEATHER
[B][C][00FFFF]   └── /weather
[B][C][FF00FF]◆ 03 ┃ [00FF7F]TRUTH
[B][C][00FFFF]   └── /truth
[B][C][FFD700]◇ 04 ┃ [00FF7F]DARE
[B][C][00FFFF]   └── /dare
[B][C][FF00FF]◆ 05 ┃ [00FF7F]CALCULATOR
[B][C][00FFFF]   └── /mth <MATH>
[B][C][FFD700]◇ 06 ┃ [00FF7F]S4 SMALL V-BADGE
[B][C][00FFFF]   └── /s4 <UID>
[B][C][FFD700]═══════════════"""
                    await safe_send_message(XX, box5, uid, chat_id, key, iv)
                    await asyncio.sleep(0.5)

                    box6 = """
[B][C][00FFFF]╭━━━━━━━━━━━━━━━━━━━━╮
[B][C][FFD700]      ✦ SAMI BD ✦
[B][C][00FF7F]       HELP CENTER
[B][C][00FFFF]╰━━━━━━━━━━━━━━━━━━━━╯
[B][C][FF00FF]◆ [00FF7F]PLAYER INFO
[B][C][00FFFF]   └── /info <UID>
[B][C][FFD700]◇ 02 ┃ [00FF7F]BAN CHECK
[B][C][00FFFF]   └── /check <UID>
[B][C][FF00FF]◆ 03 ┃ [00FF7F]AI CHAT
[B][C][00FFFF]   └── /ai <QUESTION>
[B][C][FFD700]◇ 04 ┃ [00FF7F]YOUTUBE INFO
[B][C][00FFFF]   └── /yt <CHANNEL>
[B][C][FF00FF]◆ 05 ┃ [00FF7F]TIKTOK INFO
[B][C][00FFFF]   └── /tt <USERNAME>
[B][C][FFD700]═══════════════"""
                    await safe_send_message(XX, box6, uid, chat_id, key, iv)
                    await asyncio.sleep(0.5)

                    box7 = """
[B][C][00FFFF]╭━━━━━━━━━━━━━━━━━━━━╮
[B][C][FFD700]      ✦ SAMI BD ✦
[B][C][00FF7F]       HELP CENTER
[B][C][00FFFF]╰━━━━━━━━━━━━━━━━━━━━╯
[B][C][FF00FF]◆ [00FF7F]ADD FRIEND
[B][C][00FFFF]   └── /add <uid>
[B][C][FFD700]◇ 02 ┃ [00FF7F]REMOVE FRIEND
[B][C][00FFFF]   └── /remove <uid>
[B][C][FF00FF]◆ 03 ┃ [00FF7F]S1 CRAFTLAND
[B][C][00FFFF]   └── /s1 <uid>
[B][C][FFD700]◇ 04 ┃ [00FF7F]S2 NEW V-BADGE
[B][C][00FFFF]   └── /s2 <uid>
[B][C][FF00FF]◆ 05 ┃ [00FF7F]S3 MODERATOR
[B][C][00FFFF]   └── /s3 <uid>
[B][C][FFD700]═══════════════"""
                    await safe_send_message(XX, box7, uid, chat_id, key, iv)
                    await asyncio.sleep(0.5)

                    # ── বক্স ৮: নতুন .S1 - .S11 সেকশন ──
                    box_s = """
[B][C][00FFFF]╭━━━━━━━━━━━━━━━━━━━━╮
[B][C][FFD700]      ✦ SAMI BD ✦
[B][C][00FF7F]       HELP CENTER
[B][C][00FFFF]╰━━━━━━━━━━━━━━━━━━━━╯
[B][C][FF00FF]◆ [00FF7F]BATTLE ROYALE
[B][C][00FFFF]   └── .S1
[B][C][FFD700]◇ 02 ┃ [00FF7F]BR RANK INVITE
[B][C][00FFFF]   └── .S2
[B][C][FF00FF]◆ 03 ┃ [00FF7F]ROOM RECRUIT
[B][C][00FFFF]   └── .S3
[B][C][FFD700]◇ 04 ┃ [00FF7F]INVISIBLE ROYAL
[B][C][00FFFF]   └── .S4
[B][C][FFD700]═══════════════"""
                    await safe_send_message(XX, box_s, uid, chat_id, key, iv)
                    await asyncio.sleep(0.5)

                    box8 = """
[B][C][FFD700]═══════════════
[B][C][FF00FF]◆ 05 ┃ [00FF7F]GUILD INVITE
[B][C][00FFFF]   └── .S5
[B][C][FFD700]◇ 06 ┃ [00FF7F]HUD SHARE
[B][C][00FFFF]   └── .S6
[B][C][FF00FF]◆ 07 ┃ [00FF7F]CRAFTLAND MAP
[B][C][00FFFF]   └── .S7
[B][C][FFD700]◇ 08 ┃ [00FF7F]INVISIBLE BUFF
[B][C][00FFFF]   └── .S8
[B][C][FF00FF]◆ 09 ┃ [00FF7F]RELAY MART DISCOUNT
[B][C][00FFFF]   └── .S11
[B][C][FFD700]═══════════════"""
                    await safe_send_message(XX, box8, uid, chat_id, key, iv)
                    await asyncio.sleep(0.5)

                    box9 = """
[B][C][FFD700]এই ফাইলটি তৈরি করেছেন আমাদের বড় ভাই। [B][C][FF00FF]SAMI BD পরিবারের পক্ষ থেকে ভাইকে জানাই আন্তরিক ভালোবাসা। [B][C][00FFFF]ভাইয়ের পরিশ্রম ও চেষ্টায় তৈরি হয়েছে এই সুন্দর ফাইল। [B][C][00FF7F]সবাই ফাইলটি ব্যবহার করবেন এবং আমাদের পাশে থাকবেন। [B][C][FFD700]সবার ভালোবাসা ও সহযোগিতায় এগিয়ে যাবে SAMI BD।"""
                    await safe_send_message(XX, box9, uid, chat_id, key, iv)
                    await asyncio.sleep(0.5)

                    box10 = "https://www.pella.app/home"
                    await safe_send_message(XX, box10, uid, chat_id, key, iv)

                elif inPuTMsG.strip() == '/on':
                    if str(uid) != admin_uid:
                        await safe_send_message(XX, f"[B][C][FF0000]❌ শুধু অ্যাডমিন /on ব্যবহার করতে পারবে", uid, chat_id, key, iv)
                    else:
                        bot_enabled = True
                        await safe_send_message(XX, f"[B][C][FFFFFF]✅ বট এখন চালু হয়েছে", uid, chat_id, key, iv)

                elif inPuTMsG.strip() == '/off':
                    if str(uid) != admin_uid:
                        await safe_send_message(XX, f"[B][C][FF0000]❌ শুধু অ্যাডমিন /off ব্যবহার করতে পারবে", uid, chat_id, key, iv)
                    else:
                        bot_enabled = False
                        await safe_send_message(XX, f"[B][C][FF0000]⛔ বট এখন বন্ধ করা হয়েছে", uid, chat_id, key, iv)

                elif inPuTMsG.strip() in ('/3', '/5', '/6'):
                    mode_size = int(inPuTMsG.strip()[1])
                    await safe_send_message(XX, f"[B][C][00FFFF]{mode_size} জনের টিম তৈরি করা হচ্ছে...\n", uid, chat_id, key, iv)
                    try:
                        PAc = await OpEnSq(key, iv, region)
                        await SEndPacKeT(whisper_writer, online_writer, 'OnLine', PAc)
                        await asyncio.sleep(1.0)

                        C = await Fixed_ChangeSquad(mode_size, uid, key, iv, region)
                        await SEndPacKeT(whisper_writer, online_writer, 'OnLine', C)
                        await asyncio.sleep(1.0)

                        V = await Fixed_SendInvite(mode_size, uid, key, iv, region)
                        await SEndPacKeT(whisper_writer, online_writer, 'OnLine', V)
                        await asyncio.sleep(1.0)

                        E = await ExiT(None, key, iv)
                        await asyncio.sleep(2.0)
                        await SEndPacKeT(whisper_writer, online_writer, 'OnLine', E)

                        await safe_send_message(XX, f"[B][C][00FF00]সফল! {mode_size} জনের টিমের ইনভাইট আপনার কাছে পাঠানো হয়েছে!\n", uid, chat_id, key, iv)
                    except Exception as e:
                        print_tag(f"/{mode_size} এ ত্রুটি: {e}", "red")

                elif inPuTMsG.startswith('/join '):
                    try:
                        code = inPuTMsG.split('/join ')[1].strip()
                        EM = await JoinSq_original(code, key, iv)
                        await SEndPacKeT(whisper_writer, online_writer, 'OnLine', EM)
                        await safe_send_message(XX, f"[B][C]{get_random_color()}\n✅ স্কোয়াডে জয়েন করা হয়েছে: {code}", uid, chat_id, key, iv)
                    except Exception as e:
                        print_tag(f"স্কোয়াড জয়েনে সমস্যা: {e}", "red")

                elif inPuTMsG.startswith('/exit') or inPuTMsG.startswith('/leave'):
                    await SEndPacKeT(whisper_writer, online_writer, 'OnLine', await ExiT(uid, key, iv))
                    await safe_send_message(XX, f"[B][C]{get_random_color()}\n✅ স্কোয়াড ত্যাগ করা হয়েছে", uid, chat_id, key, iv)

                elif inPuTMsG.startswith('/evos'):
                    parts = inPuTMsG.strip().split()
                    uids = [str(uid)]
                    for p in parts[1:]:
                        if p.isdigit() and len(p) >= 7: uids.append(p)
                    if evo_cycle_task and not evo_cycle_task.done():
                        evo_cycle_running = False
                        evo_cycle_task.cancel()
                        await asyncio.sleep(0.3)
                    evo_cycle_running = True
                    evo_cycle_task = asyncio.create_task(evo_gun_cycle(uids, EVO_IDS, key, iv, region))
                    await safe_send_message(XX, f"[B][C][FFFFFF]✅ ইভো সাইকেল চালু হয়েছে", uid, chat_id, key, iv)

                elif inPuTMsG.strip() == '/sevos':
                    if evo_cycle_task and not evo_cycle_task.done():
                        evo_cycle_running = False
                        evo_cycle_task.cancel()
                        await safe_send_message(XX, f"[B][C][FFFFFF]✅ ইভো সাইকেল বন্ধ করা হয়েছে", uid, chat_id, key, iv)

                elif inPuTMsG.strip().startswith('/s1'):
                    await handle_badge_command('s1', inPuTMsG, uid, chat_id, key, iv, region, XX)
                elif inPuTMsG.strip().startswith('/s2'):
                    await handle_badge_command('s2', inPuTMsG, uid, chat_id, key, iv, region, XX)
                elif inPuTMsG.strip().startswith('/s3'):
                    await handle_badge_command('s3', inPuTMsG, uid, chat_id, key, iv, region, XX)
                elif inPuTMsG.strip().startswith('/s4'):
                    await handle_badge_command('s4', inPuTMsG, uid, chat_id, key, iv, region, XX)
                elif inPuTMsG.strip().startswith('/s5'):
                    await handle_badge_command('s5', inPuTMsG, uid, chat_id, key, iv, region, XX)

                elif inPuTMsG.startswith('/evo ') and not inPuTMsG.startswith('/evos'):
                    parts = inPuTMsG.strip().split()
                    try:
                        if len(parts) < 3:
                            await safe_send_message(XX, f"[B][C][FF0000]ব্যবহার: /evo <uid> <ইমোট_নম্বর>", uid, chat_id, key, iv)
                            continue
                        emote_key = parts[-1].lower().strip()
                        uids_l = [p for p in parts[1:-1] if p.isdigit()]
                        if not uids_l:
                            await safe_send_message(XX, f"[B][C][FF0000]❌ কমপক্ষে একটি UID দাও", uid, chat_id, key, iv)
                            continue
                        emote_id = None
                        if emote_key in GENERAL_EMOTES_MAP:
                            emote_id = GENERAL_EMOTES_MAP[emote_key]
                        elif emote_key.isdigit() and int(emote_key) in EMOTE_MAP:
                            emote_id = EMOTE_MAP[int(emote_key)]
                        if emote_id is None:
                            await safe_send_message(XX, f"[B][C][FF0000]❌ ইমোট '{emote_key}' পাওয়া যায়নি", uid, chat_id, key, iv)
                            continue
                        for t in uids_l:
                            try:
                                H = await Emote_k(int(t), int(emote_id), key, iv, region)
                                await SEndPacKeT(whisper_writer, online_writer, 'OnLine', H)
                                await asyncio.sleep(0.1)
                            except Exception:
                                pass
                        await safe_send_message(XX, f"[B][C][FFFFFF]✅ ইভো ইমোট {emote_key} পাঠানো হয়েছে", uid, chat_id, key, iv)
                    except Exception as e:
                        print_tag(f"ইভো সমস্যা: {e}", "red")

                elif inPuTMsG.strip().startswith('/b '):
                    parts = inPuTMsG.strip().split()
                    bundle_ids = {"1": 914000002, "2": 914000003, "3": 914038001, "4": 914039001, "5": 914042001, "6": 914044001, "7": 914047001, "8": 914047002, "9": 914048001, "10": 914050001, "11": 914051001, "12": 914053001}
                    if len(parts) < 2:
                        await safe_send_message(XX, f"[B][C][FFFFFF]ব্যবহার: /b <১-১২>", uid, chat_id, key, iv)
                    elif parts[1] in bundle_ids:
                        bid = bundle_ids[parts[1]]
                        try:
                            anim_pkt = await animation_packet(bid, key, iv)
                            if anim_pkt and online_writer:
                                online_writer.write(anim_pkt); await online_writer.drain()
                            await asyncio.sleep(3)
                            b_pkt = await Look_Changer(bid, key, iv, look_type=1, region=region)
                            if b_pkt and online_writer:
                                online_writer.write(b_pkt); await online_writer.drain()
                            await safe_send_message(XX, f"[B][C][FFFFFF]✅ বান্ডেল {parts[1]} পাঠানো হয়েছে!", uid, chat_id, key, iv)
                        except Exception as e:
                            print_tag(f"বান্ডেল সমস্যা: {e}", "red")
                    else:
                        await safe_send_message(XX, f"[B][C][FF0000]❌ বান্ডেল খুঁজে পাওয়া যায়নি", uid, chat_id, key, iv)

                elif inPuTMsG.startswith('/e '):
                    parts = inPuTMsG.strip().split()
                    try:
                        if len(parts) < 2:
                            await safe_send_message(XX, f"[B][C][FF0000]ব্যবহার: /e <নম্বর> অথবা /e <uid> <নম্বর>", uid, chat_id, key, iv)
                            continue
                        last = parts[-1].lower().strip()
                        is_num = last in GENERAL_EMOTES_MAP
                        is_name = last in NAME_EMOTES
                        if not (is_num or is_name):
                            await safe_send_message(XX, f"[B][C][FF0000]❌ ইমোট '{last}' পাওয়া যায়নি", uid, chat_id, key, iv)
                            continue
                        tgt_uids = []
                        if len(parts) == 2:
                            tgt_uids.append(int(uid))
                        else:
                            for p in parts[1:-1]:
                                if p.isdigit():
                                    tgt_uids.append(int(p))
                        emote_id = GENERAL_EMOTES_MAP.get(last) if is_num else NAME_EMOTES.get(last)
                        sc = 0
                        for t in tgt_uids:
                            try:
                                H = await Emote_k(t, int(emote_id), key, iv, region)
                                await SEndPacKeT(whisper_writer, online_writer, 'OnLine', H)
                                sc += 1
                                await asyncio.sleep(0.1)
                            except Exception:
                                pass
                        if sc > 0:
                            await safe_send_message(XX, f"[B][C][FFFFFF]✅ {sc} জনকে ইমোট পাঠানো হয়েছে", uid, chat_id, key, iv)
                    except Exception as e:
                        print_tag(f"ইমোট সমস্যা: {e}", "red")

                elif inPuTMsG.strip().startswith('/love '):
                    try:
                        name = inPuTMsG.strip()[6:].strip()
                        msgs = [
                            f"[B][C][FF1493]❤️ {name} তুমি আমার জান! ❤️",
                            f"[B][C][FF66CC]💕 {name} তোমাকে ছাড়া কিছু নেই! 💕",
                            f"[B][C][FF00FF]💖 {name} তুমিই আমার সব! 💖",
                            f"[B][C][FF69B4]💗 {name} তুমি আমার দুনিয়া! 💗",
                            f"[B][C][FF1493]💘 {name} আমি তোমাকে অনেক ভালোবাসি! 💘",
                            f"[B][C][FF66CC]💝 {name} তুমি আমার জীবন! 💝",
                        ]
                        for m in msgs:
                            await safe_send_message(XX, m, uid, chat_id, key, iv)
                            await asyncio.sleep(1.5)
                    except Exception as e:
                        print_tag(f"ভালোবাসা সমস্যা: {e}", "red")

                elif inPuTMsG.strip().startswith('/gali '):
                    try:
                        name = inPuTMsG.strip()[6:].strip()
                        blocked = ["rafin", "rafin txt", "rafin.txt"]
                        if name.lower() in blocked:
                            await safe_send_message(XX, f"[B][C][FF0000]⚠️ বট মালিককে টার্গেট করা যাবে না!", uid, chat_id, key, iv)
                            continue
                        msgs = [
                            f"[B][C][FF0000]{name} খা🫨নক🫨ির বা🫨চ🫨্চা! 🤬",
                            f"[B][C][FF0000]{name} নো😮ংরা নাল😮ার কী😮ট! 🐛",
                            f"[B][C][FF0000]{name} ভো😮স😮ড়ি😮র! 💢",
                            f"[B][C][FF0000]{name} মা😮দার😮চো😮দ! 😡",
                            f"[B][C][FF0000]{name} ভা😮ড়ু😮য়া! 🤬",
                            f"[B][C][FF0000]{name} র🫨ান্ড😮ির বা😮চ্চা! 😤",
                            f"[B][C][FF0000]{name} নালা😮য়ে😮ক কু😮ত্তা! 🐕",
                            f"[B][C][FF0000]{name} হ😮ার😮াম😮ী! 💀",
                        ]
                        for m in msgs:
                            await safe_send_message(XX, m, uid, chat_id, key, iv)
                            await asyncio.sleep(1.5)
                    except Exception as e:
                        print_tag(f"গালি সমস্যা: {e}", "red")

                elif inPuTMsG.strip().startswith('/rt '):
                    try:
                        name = inPuTMsG.strip()[4:].strip()
                        msgs = [
                            f"[B][C][FF0000]😆 {name} তো বট, বট! 🤖",
                            f"[B][C][FF0000]🎮 {name} তো ট্রেনিং গ্রাউন্ডের পুতুল! 🗿",
                            f"[B][C][FF0000]💩 {name} এর হেডশট রেট মাইনাসে! 📉",
                            f"[B][C][FF0000]🏃 {name} তো শত্রু দেখে পালায়! 🏃‍♂️",
                            f"[B][C][FF0000]😂 {name} তো ফ্রি ফায়ারের সবচেয়ে বড় নুব! 🎯",
                            f"[B][C][FF0000]🤣 {name} এর গেমপ্লে দেখে বটরা হাসে! 😂",
                        ]
                        for m in msgs:
                            await safe_send_message(XX, m, uid, chat_id, key, iv)
                            await asyncio.sleep(1.5)
                    except Exception as e:
                        print_tag(f"রোস্ট সমস্যা: {e}", "red")

                elif inPuTMsG.strip().startswith('/praisa '):
                    try:
                        name = inPuTMsG.strip()[8:].strip()
                        msgs = [
                            f"[B][C][FFFFFF]🌟 {name} তুমি অসাধারণ মানুষ! 🌟",
                            f"[B][C][FFFFFF]🔥 {name} তোমার পরিশ্রম একদিন রঙ দেবে! 🔥",
                            f"[B][C][FFFFFF]💎 {name} তুমি ইউনিক! 💎",
                            f"[B][C][FFFFFF]🚀 {name} তোমার ভবিষ্যৎ উজ্জ্বল! 🚀",
                            f"[B][C][FFFFFF]👑 {name} তুমি লিডার হওয়ার যোগ্য! 👑",
                            f"[B][C][FFFFFF]🌈 {name} তোমার হাসি সবার দিন ভালো করে দেয়! 🌈",
                        ]
                        for m in msgs:
                            await safe_send_message(XX, m, uid, chat_id, key, iv)
                            await asyncio.sleep(0.8)
                    except Exception as e:
                        print_tag(f"প্রশংসা সমস্যা: {e}", "red")

                elif inPuTMsG.strip().startswith('/later '):
                    try:
                        name = inPuTMsG.strip()[7:].strip()
                        msg = f"[B][C][FF1493]💌 প্রিয় {name} 💌\n\nতোমার স্মৃতিতে দিন কেটে যায়,\nতোমাকে ছাড়া মন কাঁদে,\nতুমিই তো সে, যার জন্য,\nএই মন প্রতিক্ষণ ধকধক করে।\n\n💕 তোমার চিরকাল 💕"
                        await safe_send_message(XX, msg, uid, chat_id, key, iv)
                    except Exception as e:
                        print_tag(f"প্রেমপত্র সমস্যা: {e}", "red")

                elif inPuTMsG.strip() == '/joke':
                    jokes = [
                        "এক ছেলে ডাক্তারের কাছে গেল:\nডাক্তার: কী হয়েছে?\nছেলে: স্যার, যখন হাঁটি তখন ব্যথা হয়।\nডাক্তার: তাহলে হাঁটবেন না!\n😂😂",
                        "শিক্ষক: হোমওয়ার্ক কেন করনি?\nছাত্র: স্যার, কারেন্ট চলে গিয়েছিল।\nশিক্ষক: দিনে কেন করনি?\nছাত্র: দিনে তো ঘুম আসে।\n🤣",
                        "বস: তুমি ৫ বছরে কী শিখলে?\nকর্মচারী: স্যার, ৫ বছরে আমি শিখলাম যে ৫ বছর নষ্ট হয়ে গেছে!\n🤣🤣",
                        "বাচ্চা: মা, আমাকে একটা ভাই চাই।\nমা: ঠিক আছে, ভগবানের কাছে চাও।\nবাচ্চা: না, বাবার কাছে চাওয়াও, উনি ভগবানের চেয়েও বেশি দেন!\n😱😂",
                    ]
                    joke = random.choice(jokes)
                    await safe_send_message(XX, f"[B][C][FFFFFF]😂 জোকস 😂\n\n{joke}", uid, chat_id, key, iv)

                elif inPuTMsG.strip().startswith('/luck '):
                    try:
                        name = inPuTMsG.strip()[6:].strip().title()
                        predictions = [
                            f"🌟 {name} তুমি শীঘ্রই বড় সাফল্য পাবে!",
                            f"💰 {name} তোমার জীবনে অনেক টাকা আসবে!",
                            f"❤️ {name} তোমার সত্যিকারের ভালোবাসা খুব কাছে!",
                            f"🏆 {name} তুমি একদিন চ্যাম্পিয়ন হবে!",
                            f"🌈 {name} তোমার কঠিন দিন শেষ হচ্ছে!",
                            f"🎯 {name} তোমার স্বপ্ন পূরণ হবে!",
                        ]
                        p = random.choice(predictions)
                        await safe_send_message(XX, f"[B][C][FFFFFF]🔮 ভাগ্য 🔮\n\n[FFFFFF]👤 নাম: [FFFFFF]{name}\n\n[FFFFFF]{p}", uid, chat_id, key, iv)
                    except Exception as e:
                        print_tag(f"ভাগ্য সমস্যা: {e}", "red")

                elif inPuTMsG.strip() == '/quiz':
                    quizzes = [
                        ("বাংলাদেশের রাজধানী?", "ঢাকা"),
                        ("পৃথিবীর সবচেয়ে বড় মহাসাগর?", "প্রশান্ত মহাসাগর"),
                        ("বাংলাদেশের জাতীয় পাখি?", "দোয়েল"),
                        ("১ কিলোমিটার = কত মিটার?", "১০০০"),
                        ("সূর্য কোন দিক থেকে ওঠে?", "পূর্ব"),
                        ("পানির রাসায়নিক সূত্র?", "H2O"),
                        ("মানব শরীরে কতটি হাড়?", "২০৬"),
                        ("ফ্রি ফায়ারে কতজন প্লেয়ার?", "৫০"),
                    ]
                    q, a = random.choice(quizzes)
                    await safe_send_message(XX, f"[B][C][FFFFFF]🧠 কুইজ 🧠\n\n[FFFFFF]❓ {q}\n\n[FFFFFF]✅ উত্তর: {a}", uid, chat_id, key, iv)

                elif inPuTMsG.strip() == '/roll':
                    d1 = random.randint(1, 6)
                    d2 = random.randint(1, 6)
                    total = d1 + d2
                    faces = {1: "⚀", 2: "⚁", 3: "⚂", 4: "⚃", 5: "⚄", 6: "⚅"}
                    await safe_send_message(XX, f"[B][C][FFFFFF]🎲 ডাইস রোল 🎲\n\n[FFFFFF]🎯 ডাইস ১: {faces[d1]} {d1}\n[FFFFFF]🎯 ডাইস ২: {faces[d2]} {d2}\n\n[FFFFFF]📊 মোট: {total}/12", uid, chat_id, key, iv)

                elif inPuTMsG.strip() in ('/zodiac', '/rashi'):
                    signs = ["মেষ ♈", "বৃষ ♉", "মিথুন ♊", "কর্কট ♋", "সিংহ ♌", "কন্যা ♍",
                             "তুলা ♎", "বৃশ্চিক ♏", "ধনু ♐", "মকর ♑", "কুম্ভ ♒", "মীন ♓"]
                    horos = [
                        "আজ তোমার দিন দুর্দান্ত যাবে!",
                        "ভালোবাসায় আজ সুখবর আসতে পারে!",
                        "আর্থিক বিষয়ে সতর্ক থাকো।",
                        "আজ নতুন কিছু শিখবে!",
                        "স্বাস্থ্যের যত্ন নাও।",
                    ]
                    s = random.choice(signs)
                    h = random.choice(horos)
                    await safe_send_message(XX, f"[B][C][FFFFFF]🌟 রাশিফল 🌟\n\n[FFFFFF]🔮 রাশি: [FFFFFF]{s}\n\n[FFFFFF]📜 {h}", uid, chat_id, key, iv)

                elif inPuTMsG.strip() in ('/weather', '/abohawa'):
                    cities = ["ঢাকা", "চট্টগ্রাম", "খুলনা", "রাজশাহী", "সিলেট", "বরিশাল"]
                    weathers = ["☀️ রোদ", "🌤️ আংশিক মেঘ", "⛅ মেঘ", "🌧️ বৃষ্টি", "🌦️ হালকা বৃষ্টি"]
                    city = random.choice(cities)
                    temp = f"{random.randint(20, 40)}°C"
                    w = random.choice(weathers)
                    hum = f"{random.randint(40, 95)}%"
                    await safe_send_message(XX, f"[B][C][FFFFFF]🌤️ আবহাওয়া 🌤️\n\n[FFFFFF]📍 শহর: [FFFFFF]{city}\n[FFFFFF]🌡️ তাপমাত্রা: [FFFFFF]{temp}\n[FFFFFF]☁️ আবহাওয়া: [FFFFFF]{w}\n[FFFFFF]💧 আর্দ্রতা: [FFFFFF]{hum}", uid, chat_id, key, iv)

                elif inPuTMsG.strip() == '/truth':
                    truths = [
                        "💕 তুমি কাকে সবচেয়ে বেশি ভালোবাসো?",
                        "🤫 তোমার সবচেয়ে বড় সিক্রেট কী?",
                        "😭 শেষ কবে কেঁদেছিলে?",
                        "💔 তোমার ক্রাশ কে?",
                        "🤥 শেষ কবে মিথ্যা বলেছিলে?",
                        "😱 তোমার সবচেয়ে বড় ভয় কী?",
                    ]
                    t = random.choice(truths)
                    await safe_send_message(XX, f"[B][C][FFFFFF]🤔 ট্রুথ 🤔\n\n{t}", uid, chat_id, key, iv)

                elif inPuTMsG.strip() == '/dare':
                    dares = [
                        "🔥 ৫ মিনিট চোখ বন্ধ করে রাখো!",
                        "😂 পরের ১০ মিনিট শুধু হাসতে থাকো!",
                        "🐔 মুরগির মতো ডাকো!",
                        "🎤 একটা গান গাও!",
                        "💃 ৩০ সেকেন্ড নাচো!",
                    ]
                    d = random.choice(dares)
                    await safe_send_message(XX, f"[B][C][FFFFFF]🎲 ডেয়ার 🎲\n\n{d}", uid, chat_id, key, iv)

                elif inPuTMsG.strip().startswith('/mth'):
                    parts = inPuTMsG.strip().split(maxsplit=1)
                    if len(parts) < 2:
                        await safe_send_message(XX, f"[B][C][FFFFFF]ব্যবহার: /mth 2+2", uid, chat_id, key, iv)
                    else:
                        expr = parts[1].strip().replace("×", "*").replace("÷", "/").replace("x", "*")
                        try:
                            import re as _re
                            if not _re.match(r'^[\d\s\+\-\*\/\.\(\)\%]+$', expr):
                                raise ValueError("Invalid")
                            result = eval(expr)
                            if isinstance(result, float) and result == int(result):
                                result = int(result)
                            await safe_send_message(XX, f"[B][C][FFFFFF]🧮 ফলাফল: [FFFFFF]{result}", uid, chat_id, key, iv)
                        except Exception:
                            await safe_send_message(XX, f"[B][C][FF0000]❌ ভুল এক্সপ্রেশন", uid, chat_id, key, iv)

                elif inPuTMsG.strip().startswith('/info '):
                    parts = inPuTMsG.strip().split()
                    if len(parts) >= 2 and parts[1].isdigit():
                        await safe_send_message(XX, f"[B][C][FFFFFF]🔍 {parts[1]} এর তথ্য আনা হচ্ছে...", uid, chat_id, key, iv)
                        try:
                            ok, data = await get_player_info(parts[1])
                            if ok:
                                m1, m2, m3 = format_player_info(data)
                                for m in (m1, m2, m3):
                                    await safe_send_message(XX, m, uid, chat_id, key, iv)
                                    await asyncio.sleep(0.5)
                            else:
                                await safe_send_message(XX, f"[B][C][FF0000]❌ {data}", uid, chat_id, key, iv)
                        except Exception as e:
                            await safe_send_message(XX, f"[B][C][FF0000]❌ ত্রুটি: {e}", uid, chat_id, key, iv)
                    else:
                        await safe_send_message(XX, f"[B][C][FF0000]ব্যবহার: /info <uid>", uid, chat_id, key, iv)

                elif inPuTMsG.strip().startswith('/check '):
                    parts = inPuTMsG.strip().split()
                    if len(parts) >= 2 and parts[1].isdigit():
                        try:
                            ok, result = await check_banned(parts[1])
                            reply = format_check_result(result) if ok else f"[B][C][FF0000]❌ {result}"
                        except Exception as e:
                            reply = f"[B][C][FF0000]❌ ত্রুটি: {e}"
                        await safe_send_message(XX, reply, uid, chat_id, key, iv)
                    else:
                        await safe_send_message(XX, f"[B][C][FF0000]ব্যবহার: /check <uid>", uid, chat_id, key, iv)

                elif inPuTMsG.strip().startswith('/ai '):
                    question = inPuTMsG.strip()[4:].strip()
                    if question:
                        await safe_send_message(XX, f"[B][C][FFFFFF]🤖 এআই ভাবছে...", uid, chat_id, key, iv)
                        try:
                            ai_url = f"https://9x-ai.vercel.app/ask?key=RAFIN_TXT&message={question}"
                            async with aiohttp.ClientSession() as session:
                                async with session.get(ai_url, timeout=aiohttp.ClientTimeout(total=15)) as r:
                                    if r.status == 200:
                                        answer = (await r.text()).strip()
                                        msg = f"[B][C][FFFFFF]🤖 এআই উত্তর:\n\n[FFFFFF]{answer}"
                                    else:
                                        msg = f"[B][C][FF0000]❌ এআই ত্রুটি: {r.status}"
                        except Exception as e:
                            msg = f"[B][C][FF0000]❌ ত্রুটি: {e}"
                        await safe_send_message(XX, msg, uid, chat_id, key, iv)

                elif inPuTMsG.strip().startswith('/yt '):
                    channel = inPuTMsG.strip()[4:].strip()
                    if channel:
                        try:
                            url = f"https://youtube-api.vercel.app/yt?channel={channel.lstrip('@')}"
                            async with aiohttp.ClientSession() as session:
                                async with session.get(url, timeout=aiohttp.ClientTimeout(total=15)) as r:
                                    if r.status == 200:
                                        data = await r.json()
                                        stats = data.get("statistics", {})
                                        msg = f"[B][C][FFFFFF]▶️ ইউটিউব\n\n[FFFFFF]নাম: [FFFFFF]{data.get('channel_title', 'Unknown')}\n[FFFFFF]সাবস্ক্রাইবার: [FFFFFF]{stats.get('subscribers', '0')}\n[FFFFFF]ভিউ: [FFFFFF]{stats.get('views', '0')}"
                                    else:
                                        msg = f"[B][C][FF0000]❌ ইউটিউব এপিআই ত্রুটি"
                        except Exception as e:
                            msg = f"[B][C][FF0000]❌ ত্রুটি: {e}"
                        await safe_send_message(XX, msg, uid, chat_id, key, iv)

                elif inPuTMsG.strip().startswith('/tt '):
                    username = inPuTMsG.strip()[4:].strip()
                    if username:
                        try:
                            url = f"https://kawsar-tikto-info.vercel.app/tiktok?username={username}"
                            async with aiohttp.ClientSession() as session:
                                async with session.get(url, timeout=aiohttp.ClientTimeout(total=15)) as r:
                                    if r.status == 200:
                                        data = await r.json()
                                        ident = data.get("identity", {})
                                        stats = data.get("statistics", {})
                                        msg = f"[B][C][FFFFFF]🎵 টিকটক\n\n[FFFFFF]নাম: [FFFFFF]{ident.get('full_name', 'Unknown')}\n[FFFFFF]ফলোয়ার: [FFFFFF]{stats.get('followers', '0')}\n[FFFFFF]লাইক: [FFFFFF]{stats.get('likes', '0')}"
                                    else:
                                        msg = f"[B][C][FF0000]❌ টিকটক এপিআই ত্রুটি"
                        except Exception as e:
                            msg = f"[B][C][FF0000]❌ ত্রুটি: {e}"
                        await safe_send_message(XX, msg, uid, chat_id, key, iv)

                elif inPuTMsG.strip().startswith("/add ") and str(uid) == admin_uid:
                    parts = inPuTMsG.strip().split()
                    if len(parts) >= 2 and parts[1].isdigit():
                        try:
                            ok, msg = await send_friend_request(parts[1], ToKen, region)
                            reply = f"[B][C]{get_random_color()} {msg}"
                        except Exception as e:
                            reply = f"[B][C][FF0000]ত্রুটি: {e}"
                    else:
                        reply = f"[B][C][FF0000]ব্যবহার: /add <uid>"
                    await safe_send_message(XX, reply, uid, chat_id, key, iv)

                elif inPuTMsG.strip().startswith("/remove ") and str(uid) == admin_uid:
                    parts = inPuTMsG.strip().split()
                    if len(parts) >= 2 and parts[1].isdigit():
                        try:
                            ok, msg = await remove_friend(parts[1], ToKen, region)
                            reply = f"[B][C]{get_random_color()} {msg}"
                        except Exception as e:
                            reply = f"[B][C][FF0000]ত্রুটি: {e}"
                    else:
                        reply = f"[B][C][FF0000]ব্যবহার: /remove <uid>"
                    await safe_send_message(XX, reply, uid, chat_id, key, iv)

            writer.close(); await writer.wait_closed(); whisper_writer = None
        except Exception as e:
            print_tag(f"চ্যাট সমস্যা: {ip}:{port} - {e}", "red")
            whisper_writer = None
        await asyncio.sleep(reconnect_delay)


# ═══════════════════════════════════════════════════════════════
#              ★ মূল এন্ট্রি ★
# ═══════════════════════════════════════════════════════════════

async def MaiiiinE():
    global bot_uid, ToKen, region, bot_nickname, bot_clan_id

    # ✅ sami.py থেকে আসছে — এখানে আর হার্ডকোড নেই
    Uid = UID
    Pw  = PW

    print_banner()
    log("তথ্য", "লগইন প্রক্রিয়া শুরু হচ্ছে ...")
    log("তথ্য", f"লক্ষ্য অঞ্চল (Region): {REGION_PREF}")
    print()

    try:
        result = await do_login(Uid, Pw, REGION_PREF)
    except Exception as e:
        log("ত্রুটি", f"লগইনের সময় সমস্যা হয়েছে: {e}")
        return

    if not result:
        log("ত্রুটি", "লগইন ব্যর্থ হয়েছে, ১০ সেকেন্ড পর পুনরায় চেষ্টা করা হবে ...")
        await asyncio.sleep(10)
        return

    bot_uid = result["bot_uid"]
    ToKen   = result["token"]
    region  = result["region"]
    bot_nickname = result.get("account_name", "SAMI BD") or "SAMI BD"
    bot_clan_id  = result.get("clan_id", 0) or 0

    key         = result["key"]
    iv          = result["iv"]
    timestamp   = result["timestamp"]
    online_ip   = result["online_ip"]
    online_port = result["online_port"]
    chat_ip     = result["chat_ip"]
    chat_port   = result["chat_port"]
    acc_name    = result["account_name"]

    log("সফল", "লগইন সফলভাবে সম্পন্ন হয়েছে !")
    print_box(
        "SAMI BD — অ্যাকাউন্ট তথ্য",
        [
            f"\033[1;37mUID\033[0m      : \033[1;32m{result['bot_uid']}\033[0m",
            f"\033[1;37mনাম\033[0m      : \033[1;32m{acc_name}\033[0m",
            f"\033[1;37mঅঞ্চল\033[0m    : \033[1;32m{result['region']}\033[0m",
            f"\033[1;37mসার্ভার\033[0m  : \033[1;32m{online_ip}:{online_port}\033[0m",
            f"\033[1;37mচ্যাট\033[0m    : \033[1;32m{chat_ip}:{chat_port}\033[0m",
        ]
    )

    log("তথ্য", "অথেনটিকেশন টোকেন তৈরি করা হচ্ছে ...")
    ChatAutH      = create_auth_token_chat(int(result["bot_uid"]), result["token"], int(timestamp), key, iv)
    OnlineAutH, _ = build_ob55_online_auth(int(result["bot_uid"]), result["token"], int(timestamp), key, iv)
    log("সফল", "অথেনটিকেশন টোকেন সফলভাবে তৈরি হয়েছে।")

    log("অপেক্ষা", "চ্যাট সার্ভারের সাথে সংযোগ স্থাপন করা হচ্ছে ...")
    ready_event = asyncio.Event()

    t1 = asyncio.create_task(
        TcPChaT(chat_ip, chat_port, ChatAutH, key, iv, result, ready_event, result["region"])
    )
    await ready_event.wait()
    log("সফল", "চ্যাট সার্ভার সংযোগ সফল হয়েছে।")

    await asyncio.sleep(1)

    log("অপেক্ষা", "অনলাইন সার্ভারের সাথে সংযোগ স্থাপন করা হচ্ছে ...")
    t2 = asyncio.create_task(
        TcPOnLine(online_ip, online_port, key, iv, OnlineAutH)
    )

    print()
    print(c("╔" + "═" * 60 + "╗", "green"))
    print(c("║", "green") + render('BOT ONLINE', colors=['green', 'cyan'], align='center').center(62) + c("║", "green"))
    print(c("╚" + "═" * 60 + "╝", "green"))
    print()
    print_line("মালিক",  "SAMI BD")
    print_line("অঞ্চল", result['region'])
    print_line("বট UID", result['bot_uid'])
    print_line("নাম",   acc_name)
    print_line("অবস্থা", "\033[1;32m● চালু আছে\033[0m")
    print()
    print(c("▌ SAMI BD — প্রিমিয়াম TCP বট ▌", "gold").center(60))
    print(c("▌ সমস্ত সিস্টেম সচল ▌", "cyan").center(60))
    print()

    await asyncio.gather(t1, t2)


async def StarTinG():
    attempt = 0
    while True:
        attempt += 1
        try:
            log("বট", f"সেশন #{attempt} শুরু হচ্ছে — SAMI BD")
            await asyncio.wait_for(MaiiiinE(), timeout=7 * 60 * 60)
        except asyncio.TimeoutError:
            log("সতর্ক", "টোকেনের সময় শেষ হয়েছে, পুনরায় চালু করা হচ্ছে ...")
            await asyncio.sleep(3)
        except KeyboardInterrupt:
            log("সতর্ক", "ব্যবহারকারী দ্বারা বন্ধ করা হয়েছে। বিদায় !")
            sys.exit(0)
        except Exception as e:
            log("ত্রুটি", f"সমস্যা হয়েছে: {e} → ৫ সেকেন্ড পর পুনরায় চেষ্টা ...")
            await asyncio.sleep(5)


if __name__ == '__main__':
    try:
        asyncio.run(StarTinG())
    except KeyboardInterrupt:
        print(f"\n\033[1;31m▌ বট বন্ধ করা হয়েছে — SAMI BD ▌\033[0m\n")