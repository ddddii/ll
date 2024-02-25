from telethon.sync import TelegramClient, events
from telethon import events, Button
import json
import configparser
import subprocess
import telethon
import os,sys
import zipfile
from zipfile import ZipFile
from pyrogram import Client , utils, filters
import re
import requests
from database import *
from texts import *
import shutil

welcome            = "أهلا وسهلا عزيزي المشرف في لوحة التحكم\n\nلبدء عملية نقل عادية ارسل /copy\n\nلبدء عملية نقل متطورة ( للجروبات المقفولة ) ارسل /MovePro\n\n\nللفحص وعرض عدد الحسابات /check";
to_cancle           = "\nللإلغاء ارسل /cancle";
send_f_url          = "قم بإرسال الرابط الخاص أو العام للمجموعة التي سيتم نقل الأعضاء منها\nارسل رابط كالتالي\nhttps://t.me/ALRAGI1";
move_is_busy   = "هناك عملية نقل حالياً\nلإلغائها ارسل /stop_all";
send_t_url          = "✅ تم حفظ مجموعة الإضافة كالتالي\n++URL++\nقم بإرسال الرابط الخاص أو العام للمجموعة التي سيتم نقل الأعضاء إليها\nارسل رابط كالتالي\nhttps://t.me/ALRAGI1";
try_send_url       = "خطأ\nهذا ليس رابطا لجروب تيليجرام\nارسل رابط كالتالي\nhttps://t.me/ALRAGI1";
send_count        = "✅ تم حفظ مجموعة المضافين كالتالي\n++URL++\nقم بإرسال عدد الأعضاء الذي سيتم نقلهم من ++FROM++ إلى ++TO++\n\nارسل أعدادا فقط ، كالتالي\n20";
try_send_int       = "خطأ\nهذا ليس عددا صحيحا\nارسل عدد كالتالي\n22";
send_timer         = "✅ تم حفظ عدد المضافين كالتالي\n++COUNT++\nسيتم نقل ++COUNT++ من ++FROM++ إلى ++TO++\nارسل الوقت الفاصل بين كل عملية إضافة ( بالثانية ما بين 1 و 59 ) كالتالي\n5";
data_is_saved   = "✅ تم حفظ البيانات كالتالي\nسيتم نقل ++COUNT++ عضو من المجموعة ++FROM++ إلى المجموعة ++TO++ في غضون ++TIME++ ثانية\nجار الإنضمام إلى مجموعة الإضافة.....";
cancled               = "تم الإلغاء";
no_cancled        = " لا يوجد عملية لإلغائها";
checking             = "⚡️ جار فحص ++COUNT++ حسابا\n♻️ يرجى التحلي بالصبر ... يمكنك رؤية العمليات مباشرة عبر الرسالة التالية";
send_sup_url     = "⚡️ قم بإرسال رابط القناة أو المجموعة التي سيتم ضخ الأعضاء إليها......";
send_sup_count = "♻️ قم بإرسال عدد الأعضاء الذين سيتم ضخهم إلى ++URL++";
SS = "**- جاري تحميل ملف الجلسات ♻️**"
  


config = configparser.ConfigParser() 
config.read("jello.ini")

THE_SESSIONS = os.listdir('sessions');
cSessions           = len(THE_SESSIONS);

api_id       = config['owner']['id'];
api_hash = config['owner']['hash'];
client        = telethon.TelegramClient('center', api_id, api_hash);


token = config['API_KEYs']['mover'];
botID  =  int(token.split(':')[0]);
admin = config['owner']['admin'];


def zip_folder(folder_path, zip_name):
	with ZipFile(zip_name, 'w') as zipf:
		for root, _, files in os.walk(folder_path):
			for file in files:
				file_path = os.path.join(root, file)
				arc_name = os.path.relpath(file_path, folder_path)
				zipf.write(file_path, arcname=arc_name)

def move_files(source_dir, destination_dir):
    for root, _, files in os.walk(source_dir):
        for file in files:
            file_path = os.path.join(root, file)
            destination_path = os.path.join(destination_dir, file)
            shutil.move(file_path, destination_path)



def extract_zip(zip_file, extract_to):
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(extract_to)



def sendMessage(chat_id, text):
	URL	  = "https://api.telegram.org/bot"+token+"/sendmessage"
	PARAMS = {'chat_id': chat_id, 'text': text}
	RGET       = requests.get(url=URL, params=PARAMS);
	return json.loads(RGET.text)

sessions	      = os.listdir('sessions');
random.shuffle(sessions);
THE_SESSIONS = os.listdir('sessions');
cSessions	   = len(THE_SESSIONS);


bt_start     = [
		[
				Button.inline(buttonsAdder['MoveM'],'MoveM')
		],
		[
				Button.inline(buttonsAdder['JoinM'],'JoinM'),
				Button.inline(buttonsAdder['AddViews'],'AddViews')
		],
		[
				Button.inline(buttonsAdder['CheckAccounts'],'CheckAccounts'),
				Button.inline(extraButtons['Leave'],'Leave')
		],
		[
			    Button.inline(extraButtons['lists'],'lists')
		],
		[
				Button.inline(extraButtons['leaves'], 'leaves')
		]
]

bt_cancle    = [
		[
				Button.inline(extraButtons['Cancle'],'Cancle')
		],
]

bt_select      = [
		[
				Button.inline(extraButtons['MoveNormal'],'MoveNormal'),
				Button.inline(extraButtons['MovePro'],'MovePro')
		],
		[
				Button.inline(extraButtons['Back'],'Back')
		]
]

bt_back = [
		[
				Button.inline(extraButtons['Back'],'Back')
		]
]

# ازرار اضافة وحذف المجلدات 
buttonlist = [
	[
		 Button.inline(buttonsAdder['Join_list'], 'Join_list'),
		 Button.inline(buttonsAdder['Leave_list'], 'Leave_list'),
	],
	[
		 Button.inline(extraButtons['Back'],'Back'),
	],
]

client.start(bot_token=token);
client.connect();

@client.on(events.CallbackQuery())
async def callback(event):
    try:
        chat = event.original_update.peer.user_id
        fData = event.data
        data = fData.decode("utf-8")
        f_data = data.split('_')
    except:
        data = False
    from_id = str(event.sender_id)
    chat_id = event.chat_id

    status = get(from_id, 'status', 'database/mover.json')
	
    if data == 'leaves':
        await event.reply(ExtraTexts['leavestext'], parse_mode='md', buttons=bt_back)
        subprocess.Popen(["python3", "control.py", "leavesss", from_id])
        return

    if data == 'lists':
        await event.edit(ExtraTexts['textlists'], parse_mode='md', buttons=buttonlist)
        return

    if data == 'Join_list':
        await event.edit(ExtraTexts['joinlisturl'], parse_mode='md', buttons=bt_cancle)
        set(from_id, 'status', 'Joinlist', 'database/mover.json')
        return

    if data == 'Leave_list':
        await event.edit(ExtraTexts['leavelisturl'], parse_mode='md', buttons=bt_cancle)
        set(from_id, 'status', 'Leavelist', 'database/mover.json')
        return

    if data == 'MoveM':
        await event.edit(AdderTexts['selectMoveMode'], parse_mode='md', buttons=bt_select)
        return

    if data == 'Back':
        await event.edit(textsStart, buttons=bt_start, parse_mode='md')
        return

    if data == 'MoveNormal' or data == 'MovePro':
        if status is not False:
            await event.edit(move_is_busy, parse_mode='md', buttons=bt_start)
        else:
            await event.edit(AdderTexts['sendURLfrom'], buttons=bt_cancle, parse_mode='md')
            set(from_id, 'status', 'move', 'database/mover.json')
            set(from_id, 'ModeMove', data, 'database/mover.json')
        return

    if data == 'Cancle':
        await event.edit(textsStart, buttons=bt_start, parse_mode='md')
        delete(from_id, None, 'database/mover.json')
        return

    if data == 'CheckAccounts':
        subprocess.Popen(["python3", "control.py", "check", from_id])
        await event.edit(checking.replace('++COUNT++', str(cSessions)), parse_mode='md', buttons=bt_back)
        return

    if data == 'JoinM':
        if status is not False:
            await event.edit(ExtraTexts['serverIsBusy'], parse_mode='md', buttons=bt_cancle)
        else:
            await event.edit(ExtraTexts['supportCHGP'], parse_mode='md', buttons=bt_cancle)
            set(from_id, 'status', 'support', 'database/mover.json')
        return

    if f_data[0] == 'StartMove':
        OPid = f_data[1]
        subprocess.Popen(["python3", "control.py", "start", OPid])
        await event.edit(ExtraTexts['StartedMove'], buttons=bt_back, parse_mode='md')
        return

    if f_data[0] == 'StopMove':
        OPid = f_data[1]
        delete(OPid, None, 'database/users.json')
        # await event.edit(ExtraTexts['StopedMove'], buttons=bt_back, parse_mode='md')
        return

    if data == 'Leave':
        await event.edit(ExtraTexts['Leave'], buttons=bt_cancle, parse_mode='md')
        set(from_id, 'status', 'leave', 'database/mover.json')
        return

    if data == 'AddViews':
        await event.edit(ExtraTexts['ViewURL'], buttons=bt_cancle, parse_mode='md')
        set(from_id, 'status', 'viewUrl', 'database/mover.json')
        return



	
@client.on(events.NewMessage())

async def main(event):
	chattt = await event.get_chat();
	if chattt.__class__.__name__ != 'User':
		return
	try:
		b = event.message.peer_id.channel_id
		b = f"-100{b}"
	except:
		pass

	text                 = event.raw_text;
	message_id  = event.message.id;
	from_id          = str(event.sender_id);
	chat_id           = event.chat_id;
	
	if from_id == botID:
		return
	
	
	if from_id not in admin:
		#await event.reply('♻️');
		return
	status       = get(from_id,'status','database/mover.json');
	FROM       = get(from_id,'from','database/mover.json');
	TO             = get(from_id,'to','database/mover.json');
	COUNT    = get(from_id,'count','database/mover.json');
	TIMER      = get(from_id,'timer','database/mover.json');
	MMove     = get(from_id,'ModeMove','database/mover.json');
	
	if text == '/staart':
		await client.send_message(
			chat_id,
			textsStart,
			reply_markup=InlineKeyboardMarkup([
				[
					InlineKeyboardButton(buttonsAdder['MoveM'],callback_data='MoveM')
				],
				[
					InlineKeyboardButton(buttonsAdder['JoinM'],callback_data='JoinM'),
					InlineKeyboardButton(buttonsAdder['AddViews'],callback_data='AddViews')
				],
				[
					InlineKeyboardButton(buttonsAdder['CheckAccounts'],callback_data='CheckAccounts')
				],
				[
					InlineKeyboardButton(buttonsAdder['Join_list'],callback_data='Join_list'),
					InlineKeyboardButton(buttonsAdder['Leave_list'],callback_data='Leave_list')
				]
			]
		)
	)
	
	if text == '/start':
		await event.reply(textsStart,buttons=bt_start,parse_mode='md');
		return
	if text == '/list':
		await event.reply(ExtraTexts['textlists'], buttons=buttonlist, parse_mode='md');
		return
	
	if text == '/session':
		await event.reply(textsStart,buttons=bt_start,parse_mode='md');
		return
	
	if text == '/get':
		await event.reply(ExtraTexts['getnum'], parse_mode='md')
		subprocess.Popen(["python3", "control.py", "getN", from_id])
		return
	

	#if text == '/gett':
	#	await event.reply(ExtraTexts['getnum'], parse_mode='md')
	#	random_file = random.choice(sessions)
	#	opID       = makeKey();
	#	num = Client(f"{random_file}",api_id=api_id, api_hash=api_hash)
	#	con = await num.connect()
	#	Con = num.get_me()
	#	B = num.session_string
	#	A = num.phone_number
	#	TEXT = f"- تم أختيار الرقم بنجاح ✅.\n- الرقم  : `{A}`\n - قم بطلب الكود ثم أضغط الزر بالاسغل."
	#	set(from_id,'owner', from_id, 'database/mover.json');
	#	set(from_id,'NUM', A, 'database/mover.json');
	#	set(from_id,'file', random_file, 'database/mover.json')
	#	set(from_id,'sessions', str(B), 'database/mover.json');
	#	#setfrom_idD,'sess', num, 'database/mover.json');
	#	set(from_id, 'status', 'get', 'database/mover.json')
	#	#subprocess.Popen(["python3", "control.py", "getN", from_id])
	#	return
	
	if text and status == 'get':
		file = get(from_id,'file','database/mover.json');
		id = get(from_id,'owner','database/mover.json')
		NUMM = get(from_id,'NUM','database/mover.json')
		sess = get(from_id,'sessions','database/mover.json')
		key = [
			[
				Button.inline("- جلب الكود 😁", f'Get{NUMM}'),
				Button.inline(extraButtons['Cancle'],'Cancle')
			]
		]
		GETNUM = f"- تم أختيار الرقم بنجاح ✅.\n- الرقم  : `{NUMM}`\n - قم بطلب الكود ثم أضغط الزر بالاسغل."
		await event.edit(GETNUM, parse_mode='md', buttons=key)
		return


	if text == '/cancle':
		if status is not False:
			delete(from_id,None,'database/mover.json');
			await event.reply(cancled);
		else:
			await event.reply(no_cancled);
		return
	
	if text == '/sessions':
		entity = await event.get_input_sender()
		await event.reply(SS, parse_mode='md')
		zip_folder("sessions", "sessions.zip")
		await client.send_file(entity=entity,file="sessions.zip", caption="The Sessions")
		return
	
	if text == '/reaction':
		await event.reply(ExtraTexts['reactiontext'], parse_mode='md', buttons=bt_cancle)
		set(from_id,'status','reaction','database/mover.json')
		return
	
	if text and status == 'reaction':
		regExNu   = re.findall("^https?:\/\/t\.me\/([a-zA-Z0-9_]+)\/([0-9]+)",text);
		if len(regExNu) > 0:
			opID = makeKey()
			UNCC    = '@'+str(regExNu[0][0]);
			IDCC      = regExNu[0][1]
			set(from_id,'username_reaction',UNCC,'database/mover.json');
			set(from_id,'ID_reaction',IDCC,'database/mover.json');
			set(from_id,'status','reactionnum','database/mover.json');
			await event.reply(ExtraTexts['reactioncount'],buttons=bt_cancle,parse_mode='md');
			return
		
	if text and status == 'reactionnum':
		regExNu = re.findall("^[0-9]+$", text)
		if len(regExNu) > 0:
			set(from_id,'count_reaction',text,'database/mover.json');
			#us = get(from_id, 'username_reaction', 'database/mover.json')
			#idc = get(from_id, 'ID_reaction', 'database/mover.json')
			set(from_id,'status','reactionemogi','database/mover.json');
			await event.reply(ExtraTexts['reactionemogi'], buttons=bt_back, parse_mode='md')
			return
	
	if text and status == 'reactionemogi':
		us = get(from_id, 'username_reaction', 'database/mover.json')
		idc = get(from_id, 'ID_reaction', 'database/mover.json')
		em = get(from_id, 'count_reaction', 'database/mover.json')
		await event.reply(ExtraTexts['reactioning'], buttons=bt_back, parse_mode='md')
		run_script(f"python3 control.py reaction {us} {idc} {from_id} {text} {em}")
		delete(from_id, None, 'database/mover.json')
		return


	if text == '/poll':
		await event.reply(ExtraTexts['polltext'], parse_mode='md', buttons=bt_cancle)
		set(from_id,'status','poll','database/mover.json')
		return
	
	if text and status == 'poll':
		regExNu   = re.findall("^https?:\/\/t\.me\/([a-zA-Z0-9_]+)\/([0-9]+)",text);
		if len(regExNu) > 0:
			opID = makeKey()
			UNCC    = '@'+str(regExNu[0][0]);
			IDCC      = regExNu[0][1]
			set(from_id,'username_poll',UNCC,'database/mover.json');
			set(from_id,'ID_poll',IDCC,'database/mover.json');
			set(from_id,'status','pollCount','database/mover.json');
			await event.reply(ExtraTexts['pollcount'],buttons=bt_cancle,parse_mode='md');
			return
		
	if text and status == 'pollCount':
		regExNu   = re.findall("^[0-9]+$",text);
		if len(regExNu) > 0:
			set(from_id,'pollcount',text,'database/mover.json');
			await event.reply(ExtraTexts['pollnum'],buttons=bt_cancle,parse_mode='md');
			set(from_id,'status','pollnum','database/mover.json');
			return
		
	if text and status == 'pollnum':
		regExNu = re.findall("^[0-9]+$", text)
		if len(regExNu) > 0:
			d = str(regExNu[0])
			us = get(from_id, 'username_poll', 'database/mover.json')
			idc = get(from_id, 'ID_poll', 'database/mover.json')
			po = get(from_id, 'pollcount', 'database/mover.json')
			await event.reply(ExtraTexts['polling'], buttons=bt_back, parse_mode='md')
			run_script(f"python3 control.py Poll {us} {idc} {po} {from_id} {text}")
			delete(from_id, None, 'database/mover.json')
			return




	#if text and status == 'get':
	#	try:
	#		zip_folder("sessionss", "sessions.zip")
	#		await client.send_file(entity=from_id,file="sessions.zip", caption="The Sessions")


	if text == '/support':
		if status is not False:
			await event.reply(move_is_busy);
		else:
			await event.reply(send_sup_url+to_cancle);
			set(from_id,'status','support','database/mover.json');
		return
		
	if text and status == 'Joinlist':
		regExNu = re.findall("^https:\/\/t\.me\/addlist\/([a-zA-Z0-9_]+)$", text);
		if len(regExNu) > 0:
			opID = makeKey();

			listID = text
			IDlist = regExNu[0][1];
			await event.reply(ExtraTexts['ListJoin'], parse_mode='md', buttons=bt_back);
			set(opID,'owner', from_id, 'database/list.json');
			set(opID,'linklist', listID, 'database/list.json');
			set(opID,'list_link', IDlist, 'database/list.json');
			run_script(f"python3 control.py JoinList {opID} {text} {listID} {IDlist} {from_id}");
			#subprocess.Popen(["python3", "control.py", "JoinList", text, from_id]);
		else:
			await event.reply(ExtraTexts['listcancle'], parse_mode='md', buttons=bt_back);
		return
	
	if text and status == 'Leavelist':
		regExNu = re.findall("^https:\/\/t\.me\/addlist\/([a-zA-Z0-9_]+)$", text);
		if len(regExNu) > 0:
			opID = makeKey();

			await event.reply(ExtraTexts['ListLeave'], parse_mode='md', buttons=bt_cancle);
			set(opID,'owner', from_id, 'database/list.json');
			set(opID,'linklists', text, 'database/list.json');
			run_script(f"python3 control.py LeaveList {opID} {text} {from_id}");
			#subprocess.Popen(["python3", "control.py", "LeaveList", text, from_id]);
		else:
			await event.reply(ExtraTexts['listcancle'], parse_mode='md', buttons=bt_back);
		return

	if text == '/check':
		###run_script(f"python3 control.py check {from_id}");
		subprocess.Popen(["python3", "control.py", "check",from_id]);
		await event.reply(checking.replace('++COUNT++',str(cSessions)));
	if text == '/copy' or text == '/MovePro':
		if status is not False:
			await event.reply(move_is_busy);
		else:
			await event.reply(send_f_url+to_cancle);
			set(from_id,'status','move','database/mover.json');
			set(from_id,'ModeMove',text,'database/mover.json');
		return
	if text and status == 'move':
		test_url    = URLc(text);
		if test_url is not False:
			rp_text     = AdderTexts['sendURLto'];
			await event.reply(rp_text,parse_mode='md',buttons=bt_cancle);
			set(from_id,'status','adding_group','database/mover.json');
			set(from_id,'from',text,'database/mover.json');
			return
		else:
			await event.reply(try_send_url,parse_mode='md',buttons=bt_cancle);
	if text and status == 'adding_group':
		test_url    = URLc(text);
		if test_url is not False:
			rp_text   = AdderTexts['sendCount'].replace('++TO++',text).replace('++FROM++',FROM);
			await event.reply(rp_text,parse_mode='md',buttons=bt_cancle);
			set(from_id,'status','select_members','database/mover.json');
			set(from_id,'to',text,'database/mover.json');
		else:
			await event.reply(try_send_url,parse_mode='md',buttons=bt_cancle);
		return
	if text and status == 'select_members':
		regExNu   = re.findall("^[0-9]+",text);
		if len(regExNu) > 0:
			rp_text   = AdderTexts['sendTime'];
			await event.reply(rp_text,parse_mode='md',buttons=bt_cancle);
			set(from_id,'status','set_timer','database/mover.json');
			set(from_id,'count',text,'database/mover.json');
		else:
			await event.reply(try_send_int,parse_mode='md',buttons=bt_cancle);
		return
	if text and status == 'set_timer':
		regExNu   = re.findall("^[0-9]+",text);
		if len(regExNu) > 0:
			rp_text   = AdderTexts['Joining'].replace('++TO++',TO).replace('++FROM++',FROM).replace('++COUNT++',str(COUNT)).replace('++TIME++',str(text));
			await event.reply(rp_text,parse_mode='md',buttons=bt_cancle);
			delete(from_id,'status','database/mover.json');
			set(from_id,'timer',text,'database/mover.json');
			opID       = makeKey();
			
			if MMove == 'MovePro':
				run_script(f"python3 control.py joinPro {opID} {from_id} {FROM} {TO} {COUNT} {text}");
			else:
				run_script(f"python3 control.py join {opID} {from_id} {FROM} {TO} {COUNT} {text}");
				
			delete(from_id,None,'database/mover.json');
		else:
			await event.reply(try_send_int+to_cancle);
		return
	if text.split('_')[0] == '/move':
		opreatID   = text.split('_')[1];
		#run_script(f"python3 control.py start {opreatID}");
		subprocess.Popen(["python3", "control.py", "start", opreatID]);
		#await event.reply(checking);
	
	if text and status == 'viewUrl':
		regExNu   = re.findall("^https?:\/\/t\.me\/([a-zA-Z0-9_]+)\/([0-9]+)",text);
		if len(regExNu) > 0:
			UNC    = '@'+str(regExNu[0][0]);
			IDC      = regExNu[0][1];
			set(from_id,'username_view',UNC,'database/mover.json');
			set(from_id,'ID_view',IDC,'database/mover.json');
			set(from_id,'status','viewCount','database/mover.json');
			await event.reply(ExtraTexts['ViewCount'],buttons=bt_cancle,parse_mode='md');
			return
	
	if text and status == 'viewCount':
		regExNu   = re.findall("^[0-9]+$",text);
		if len(regExNu) > 0:
			ugn    = get(from_id,'username_view','database/mover.json');
			idn      = get(from_id,'ID_view','database/mover.json');
			await event.reply(ExtraTexts['Viewing'],buttons=bt_back,parse_mode='md');
			subprocess.Popen(["python3", "control.py", "View", ugn, idn, text, from_id]);
			delete(from_id,None,'database/mover.json');
			return
	
			
	if text and status == 'leave':
		regExNu   = re.findall("^\-[0-9]+",text);
		if len(regExNu) > 0:
			await event.reply(ExtraTexts['Leaved'],buttons=bt_back);
			subprocess.Popen(["python3", "control.py", "leaveChat", text]);
			delete(from_id,None,'database/mover.json');
	

	


	

	if text and status == 'support':
		test_url    = URLc(text);
		if test_url is not False:
			await event.reply(send_sup_count.replace('++URL++',test_url[1]),parse_mode='md',buttons=bt_cancle);
			set(from_id,'status','select_sup_members','database/mover.json');
			set(from_id,'username_sup',test_url[1],'database/mover.json');
		else:
			await event.reply(try_send_url+to_cancle);
		return
	if text and status == 'select_sup_members':
		regExNu   = re.findall("^[0-9]+",text);
		if len(regExNu) > 0:
			opID       = makeKey();
			set(opID,'owner',from_id,'database/support.json');
			set(opID,'requested_count',text,'database/support.json');
			set(opID,'supported_username',get(from_id,'username_sup','database/mover.json'),'database/support.json');
			run_script(f"python3 control.py joining {opID}");
			delete(from_id,None,'database/mover.json');
		else:
			await event.reply(try_send_int,parse_mode='md',buttons=bt_cancle);
		return


client.run_until_disconnected();


