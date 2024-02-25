import os, asyncio, shutil, traceback
from zipfile import ZipFile

from pyrogram import Client, filters, compose, idle
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyromod import listen

from pyrogram.errors import SessionPasswordNeeded, PhoneCodeExpired
from pyrogram.errors.exceptions.bad_request_400 import PasswordHashInvalid,PhoneCodeInvalid
from pyrogram.errors.exceptions.not_acceptable_406 import PhoneNumberInvalid

from pyrogram.raw.functions.chatlists import CheckChatlistInvite, JoinChatlistInvite,LeaveChatlist
from pyrogram.raw.types import InputChatlistDialogFilter
from pyrogram.utils import get_peer_id

token = "6423878412:AAG5DfcXrwJbvAuAVxvmtiQLsvdRfMPU7h0"
api_id = 19312827
api_hash = "84da7f08e87849853b2fa6728e4192a2"

allwod_ids=["5894339732", "2095495680"]

app = Client("Bot-Sessions/bot-2", api_id=api_id, api_hash=api_hash, bot_token=token)
#——————–——–———————————––#
async def sessions_num():
	try:
		
		files = os.listdir("Sessionss")
		path = "Sessionss"
		file_list = [f for f in files if os.path.isfile(os.path.join(path, f)) and not f.endswith(".session-journal")]
		file_count = len(file_list)

		return file_count
	except Exception as e:
		print(f"Error counting files: {e}")
		return None
#——————–——–———————————––#
async def copy_file(source_path, destination):
	try:
		shutil.copy(source_path, destination)
		return (f"File copied successfully from {source_path} to {destination}")
	except FileNotFoundError:
		return ("Source file not found.")
	except PermissionError:
		return ("Permission error. Make sure you have the necessary permissions.")
	except Exception as e:
		return (f"An error occurred: {e}")
#——————–——–———————————––#
def zip_folder(folder_path, zip_name):
	with ZipFile(zip_name, 'w') as zipf:
		for root, _, files in os.walk(folder_path):
			for file in files:
				file_path = os.path.join(root, file)
				arc_name = os.path.relpath(file_path, folder_path)
				zipf.write(file_path, arcname=arc_name)
#——————–——–———————————––#
async def remove_session_journals():
	paths = ["Sessions","Sessionss"]
	for path in paths:
		try:
			for filename in os.listdir(path):
				if filename.endswith(".session-journal"):
					file_path = os.path.join(path, filename)
					os.remove(file_path)
					msg=(f"Removed: {file_path}")
			msg = ("Cleanup completed.")
		except FileNotFoundError:
			msg = (f"Path not found: {path}")
		except PermissionError:
			msg=("Permission error.Make sure you have the necessary permissions.")
		except Exception as e:
			msg =  (f"An error occurred: {e}")
	return msg
#——————–——–———————————––#
async def accounts():
    sessions_folder = "Sessionss"
    session_files = [file for file in os.listdir(sessions_folder) if os.path.isfile(os.path.join(sessions_folder, file))]
    
    apps = [
    ]
    for session_name in session_files:
        if session_name.endswith(".session-journal"):continue
        session_path = os.path.join(sessions_folder, session_name.replace(".session", ""))
        app = Client(api_id=api_id, api_hash=api_hash, name=session_path)
        apps.append(app)
    print(apps)
    await compose(apps)
    return apps
#——————–——–———————————––#
async def join_chatlist(client, invite):
	hash = invite.split("/")[-1]
	chats = await client.invoke(CheckChatlistInvite(slug=hash))
	await client.invoke(
		JoinChatlistInvite(
			slug=hash,
			peers=[await client.resolve_peer(get_peer_id(c)) for c in chats.peers]
		)
	)

async def leave_chatlist(client, invite):
  hash = invite.split('/')[-1]
  info = await client.invoke(CheckChatlistInvite(slug=hash))
  await client.invoke(
	LeaveChatlist( chatlist=InputChatlistDialogFilter(filter_id=info.filter_id),
	  peers=[await client.resolve_peer(get_peer_id(c)) for c in info.already_peers]
	)
  )
#——————–——–———————————––#
async def join_channel(client, invite):
	invite=invite.replace("https://t.me/","@")
	invite=invite.replace("t.me/","@")
	return await client.join_chat(invite)

async def leave_channel(client, invite):
	invite=invite.replace("https://t.me/","@")
	invite=invite.replace("t.me/","@")
	return await client.leave_chat(invite)
#——————–——–———————————––#
async def leave_all_chats(acc):
	async for dialog in acc.get_dialogs():
		chat_type = dialog.chat.type.value
		print(chat_type)
		if chat_type == "channel" or chat_type == "group" or chat_type == "supergroup":
			iD = str(dialog.chat.id)
			await acc.leave_chat(iD)
#——————–——–———————————––#
async def check_accs(chat_id,check):
	apps = await accounts()
	good = 0;bad = 0
	for acc in apps:
		try:
			#await acc.start()
			m = await acc.send_message('me','test')
			print(m)
			await acc.delete_messages('me', m.id)
			#await acc.stop()
			good += 1
		except Exception as e:
			file = os.path.join(acc.name+".session")
			#os.remove(file)
			bad += 1
			traceback.print_exc()
			exit()
	if check is True:
		await app.send_message(
	text=f"تم التحقق من جميع الحسابات بنجاح:\nعدد الحسابات التي تعمل: {good}\nعدد الحسابات التي لا تعمل: {bad}",
	chat_id=chat_id)
#——————–——–———————————––#
@app.on_message(filters.command("start"))
async def start_command(client, message):
	chat_id = message.from_user.id
	if str(chat_id) not in allwod_ids:return
	inline_keyboard = [
	[InlineKeyboardButton("إضافة حساب", callback_data="add_acc")],
	[InlineKeyboardButton("خروج من مجلد", callback_data='leave_list')
	,InlineKeyboardButton("دخول مجلد", callback_data='join_list')],
	[InlineKeyboardButton("خروج من قناة", callback_data='leave_channel'),
	InlineKeyboardButton("دخول قناة", callback_data='join_channel')],
	[InlineKeyboardButton("خروج من جميع القنوات", callback_data="leave_all")],
	[InlineKeyboardButton("تحقق من جميع الحسابات", callback_data="check_accs")]
	]
	reply_markup = InlineKeyboardMarkup(inline_keyboard)
	##await remove_session_journals()
	sess_num = await sessions_num()
	await client.send_message(
		chat_id=message.from_user.id,
		text=f"عدد الحسابات في البوت: {sess_num}\nاختر ما تريد من الاسفل:",
		reply_markup=reply_markup
	)
#——————–——–———————————––#
@app.on_callback_query()
async def handle_callback_query(client, callback_query):
	#await remove_session_journals()
	data = callback_query.data
	msg = callback_query.message
	chat_id = callback_query.from_user.id
	if data == 'add_acc':
		sess_num = await sessions_num()
		name=f"ses-{(sess_num+1)}"
		c = Client(
			f"Sessions/{name}",
			api_id, api_hash,
			device_model="Pyrogram"
		)
		await c.connect()
		
		phone_ask = await msg.chat.ask(
		"ارسل رقم الهاتف مع رمز الدولة:",
		filters=filters.text
		)
		phone = phone_ask.text

		try:
			send_code=await c.send_code(phone)
		except PhoneNumberInvalid:
			return await phone_ask.reply("رقم الهاتف غير صحيح", quote=True)
		except Exception:
			return await phone_ask.reply("حدث خطأ جرب مرة اخرى", quote=True)
		hash = send_code.phone_code_hash
		code_ask = await msg.chat.ask(
		"ارسل الكود الذي وصلك:\n[!] اذا كنت داخل الحساب الذي تسجل به الان فأدخل الكود مع وضع مسافات بين الارقام مثال: 1 2 3 4 5", 
		filters=filters.text
		)
		code = code_ask.text
		code = code.replace(" ","")
		try:
			await c.sign_in(phone, hash, code)
		except SessionPasswordNeeded:
			password_ask = await msg.chat.ask("ارسل كلمة سر الحساب:", filters=filters.text)
			password = password_ask.text
			try:
				await c.check_password(password)
			except PasswordHashInvalid:
				return await password_ask.reply("كلمة السر غير صالحة يرجى اعادة تسجيل الدخول من البداية", quote=True)
		except (PhoneCodeInvalid, PhoneCodeExpired):
			return await code_ask.reply("رمز تسجيل الدخول غير صحيح يرجى تسجيل الدخول من البداية", quote=True)
		try:
			await c.sign_in(phone, hash, code)
		except Exception:pass
		get = await c.get_me()
		text = '**✅ تم تسجيل الدخول بنجاح\n'
		text += f'👤 الاسم الأول : {get.first_name}\n'
		text += f'🆔 بطاقة تعريف : {get.id}\n'
		text += f'📞 رقم الهاتف : {phone}\n'
		text += '\n/start'
		await app.send_message(msg.chat.id, text)
		await copy_file(f"Sessions/{name}.session", f"Sessionss/{name}.session")
		#await remove_session_journals()
		return
#——————–——–———————————––#
	elif data == 'join_list':
		list_ask = await msg.chat.ask(
		"ارسل رابط المجلد:",
		filters=filters.text
		)
		list_invite = list_ask.text
		apps = await accounts()
		try:
			done = 0;bad = 0
			for acc in apps:
				try:
					await acc.start()
					await join_chatlist(acc,list_invite)
					await acc.stop()
					done += 1
				except Exception as e:
					bad += 1
					print(e)
					import traceback
					traceback.print_exc()
			#await remove_session_journals()
			await client.send_message(
			text=f"تم دخول المجلد مع:\nعدد الحسابات الناجحة: {done}\nعدد الحسابات غير الناجحة: {bad}",
			chat_id=chat_id)
		except Exception:
			await client.send_message(
			text="حدث خطأ اثناء دخول المجلد",
			chat_id=chat_id)
		#await remove_session_journals()
		return
	elif data == 'leave_list':
		list_ask = await msg.chat.ask(
		"ارسل رابط المجلد:",
		filters=filters.text
		)
		list_invite = list_ask.text
		apps = await accounts()
		try:
			done = 0;bad = 0
			for acc in apps:
				try:
					await acc.start()
					await leave_chatlist(acc,list_invite)
					await acc.stop()
					done += 1
				except Exception as e:
					bad += 1
					print(e)
					import traceback
					traceback.print_exc()
			await client.send_message(
			text=f"تم الخروج من المجلد مع:\nعدد الحسابات الناجحة: {done}\nعدد الحسابات غير الناجحة: {bad}",
			chat_id=chat_id)
		except Exception:
			await client.send_message(
			text="حدث خطأ اثناء حذف المجلد",
			chat_id=chat_id)
		#await remove_session_journals()
		return
#——————–——–———————————––#
	elif data == 'join_channel':
		link_ask = await msg.chat.ask(
		"ارسل رابط القناة:",
		filters=filters.text
		)
		link = link_ask.text
		apps = await accounts()
		try:
			done = 0;bad = 0
			for acc in apps:
				try:
					await acc.start()
					await join_channel(acc,link)
					await acc.stop()
					done += 1
				except Exception as e:
					bad += 1
					print(e)
					import traceback
					traceback.print_exc()
			#await remove_session_journals()
			await client.send_message(
			text=f"تم دخول القناة مع:\nعدد الحسابات الناجحة: {done}\nعدد الحسابات غير الناجحة: {bad}",
			chat_id=chat_id)
		except Exception:
			await client.send_message(
			text="حدث خطأ اثناء دخول القناة",
			chat_id=chat_id)
		#await remove_session_journals()
		return
	elif data == 'leave_channel':
		link_ask = await msg.chat.ask(
		"ارسل رابط القناة:",
		filters=filters.text
		)
		link = link_ask.text
		apps = await accounts()
		try:
			done = 0;bad = 0
			for acc in apps:
				try:
					await acc.start()
					await leave_channel(acc,link)
					await acc.stop()
					done += 1
				except Exception as e:
					bad += 1
					print(e)
					import traceback
					traceback.print_exc()
			#await remove_session_journals()
			await client.send_message(
			text=f"تم الخروج من القناة مع:\nعدد الحسابات الناجحة: {done}\nعدد الحسابات غير الناجحة: {bad}",
			chat_id=chat_id)
		except Exception:
			await client.send_message(
			text="حدث خطأ اثناء خروج من القناة",
			chat_id=chat_id)
		#await remove_session_journals()
		return
#——————–——–———————————––#
	elif data == 'leave_all':
		cnf_ask = await msg.chat.ask(
		"هل انت متأكد\nارسل [نعم - لا]",
		filters=filters.text
		)
		cnf = cnf_ask.text
		if cnf != "نعم":return
		apps = await accounts()
		try:
			done = 0;bad = 0
			for acc in apps:
				try:
					await acc.start()
					await leave_all_chats(acc)
					await acc.stop()
					done += 1
				except Exception as e:
					bad += 1
					print(e)
					import traceback
					traceback.print_exc()
			#await remove_session_journals()
			await client.send_message(
			text=f"تم الخروج من جميع القنوات مع:\nعدد الحسابات الناجحة: {done}\nعدد الحسابات غير الناجحة: {bad}",
			chat_id=chat_id)
		except Exception:
			await client.send_message(
			text="حدث خطأ اثناء خروج من القنوات",
			chat_id=chat_id)
		#await remove_session_journals()
		return
	elif data == 'check_accs':
		await check_accs(chat_id,True)
	#await remove_session_journals()
#——————–——–———————————––#
@app.on_message(filters.command("sessions"))
async def sessions_command(client, message):
	chat_id = message.from_user.id
	await check_accs(chat_id,True)
	if str(chat_id) not in allwod_ids:return
	zip_folder("Sessionss", "sessions.zip")
	#await remove_session_journals()
	await client.send_document(
		chat_id=message.from_user.id,
		document="sessions.zip",
		caption="ملف الجلسات:"
		)


print("started")
app.run()