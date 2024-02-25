from pyrogram import Client , utils, filters, compose
from pyrogram.raw import functions, types, base
import sys, time
import asyncio
import json
import configparser
import requests
from pyrogram.errors import FloodWait, UserPrivacyRestricted, UserRestricted, PeerFlood, UserNotMutualContact, UserChannelsTooMuch
from pyrogram.raw.functions.chatlists import CheckChatlistInvite, JoinChatlistInvite,LeaveChatlist
from pyrogram.raw.types import InputChatlistDialogFilter
from database import *
from pyrogram.utils import get_peer_id
from pyrogram.raw.base import input_peer
from pyrogram.raw.functions.messages import AddChatUser

opreat      = sys.argv[1];
opreats    = ['addusers','join','left','Poll','copy','check','send','reaction','Get','ass','leftgroup','leftchannels','leavess','getusers','adduser','getUsers','joining','CX','MovePro','View','AddUser','joinlist','leavelist'];
LIST_DONE    = "✅ تم اضافة المجلد بنجاح\nرابط المجلد  : ++CC++\nعدد الحسابات التي اضافة المجلد بنجاح ++ADD++ من اصل ++ALL++";
LEAVE_RUN    = "جاري حذف المجلد...... ♻️\n عدد الحسابات التي حذفت المجلد بنجاح لحد الان ++LEA++ حساب من اصل ++ALL++ حساب ✅.";
LEAVE_DONE   = "تم الانتهاء من عملية حذف المجلد بنجاح ✅\nعدد الحسابات الذي حذفت المجلد بدون مشاكل ++LEA++ حساب من أصل ++ALL++ حساب 😊.";
JOINED       = "🎢 جاري اضافة المجلد....\n♻️ يتم اضافة المجلد ++CC++ من جميع الحسابات المتاحة\n✅ تم اضافة المجلد بنجاح من ++ADD++ حساب";



if opreat not in opreats:
	exit();

ses    = sys.argv[2].split('.')[0];



config = configparser.ConfigParser()
config.read("jello.ini")



api_id       = config['owner']['id'];
api_hash = config['owner']['hash'];
token	= config['API_KEYs']['mover'];

sessions	      = os.listdir('sessions');
random.shuffle(sessions);
THE_SESSIONS = os.listdir('sessions');
cSessions	   = len(THE_SESSIONS);




def sendMessage(chat_id, text):
	URL	  = "https://api.telegram.org/bot"+token+"/sendmessage"
	PARAMS = {'chat_id': chat_id, 'text': text}
	RGET       = requests.get(url=URL, params=PARAMS);
	return json.loads(RGET.text)

def editMessage(chat_id,text,message_id):
	URL	   = "https://api.telegram.org/bot"+token+"/editMessageText";
	PARAMS  = {'chat_id': chat_id, 'text': text, 'message_id': message_id};
	RGET       = requests.get(url=URL, params=PARAMS);
	TG_RESPONSE     = False;
	try:
		TG_RESPONSE   =  json.loads(RGET);
	except:
		return TG_RESPONSE;
	return TG_RESPONSE;


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


async def leave_all_chats(acc):
	async for dialog in acc.get_dialogs():
		chat_type = dialog.chat.type.value
		print(chat_type)
		if chat_type == "channel" or chat_type == "group" or chat_type == "supergroup":
			iD = str(dialog.chat.id)
			await acc.leave_chat(iD)

async def leave_all_group(acc):
	async for dialog in acc.get_dialogs():
		chat_type = dialog.chat.type.value
		print(chat_type)
		if chat_type == "group" or chat_type == "supergroup":
			iD = str(dialog.chat.id)
			await acc.leave_chat(iD)

async def leave_all_channels(acc):
	async for dialog in acc.get_dialogs():
		chat_type = dialog.chat.type.value
		print(chat_type)
		if chat_type == "channel":
			iD = str(dialog.chat.id)
			await acc.leave_chat(iD)


async def Controll():
	try:
		app	  = Client(f"sessions/{ses}",api_id=api_id, api_hash=api_hash);		connect  = await app.connect();

		if opreat == 'check':
			try:
				await app.get_me();
				print('true');
			except:
				print('false');

		await app.get_me();
	except Exception as Errors:
		RESPONSE      = str(Errors).replace('Telegram says: ', '').split(' - ')[0];

		if RESPONSE in ['[401 AUTH_KEY_UNREGISTERED]', '[401 USER_DEACTIVATED]', '[401 USER_DEACTIVATED_BAN]', '[401 SESSION_REVOKED]']:
			try:
				print('deleted');
				os.remove(f"sessions/{ses}.session");
			except:
				pass
		if opreat == 'check':
			print(RESPONSE);
		print('false',Errors);
		connect   = False;
		#print(ses);
		return
	if not connect:
		print('NO_CONNECTED');
		return

	try:
		await app.invoke(functions.account.UpdateStatus(
			offline=False
		));
	except:
		pass

	if opreat == 'CX':
		
		UNChat     = "phpmm"
		IDsUsers    = [];
		ListUsers   = [];
		
		async for message in app.get_chat_history(UNChat):
			if message.from_user.username is not None:
				print(message.from_user.username);


	if opreat == 'join':
		urlF	 = sys.argv[3];
		urlL	 = sys.argv[4];
		
		URL_f     = URLc(urlF)[1];
		if urlF == urlL:
			URL_l  = URL_f;
		else:
			URL_l  = URLc(urlL)[1];
		print(URL_f,URL_l);

		try:
			joinF    = await app.join_chat(URL_f);
			if urlF == urlL:
				joinF = joinL;
			else:
				joinL  = await app.join_chat(URL_l);
			print('true');
			print(joinF.id);
			print(joinL.id);
		except Exception as Error:
			RESPONSE      = str(Error).replace('Telegram says: ', '').split(' - ')[0];
			if RESPONSE is not False:
				print('true');
				print(9000);
				print(9000);
			else :
				print('false',Error);
			pass

	
	if opreat == 'ass':
		k = sys.argv[3]
		key = sys.argv[5]
		users = []
		try:
			chats =  app.get_chat_members(k)
			async for User in chats:
				if User.user.username is not None:
						y =  app.get_users(User.user.username)
						h = y.is_premium
						if h == True:
							users.append(f"@{User.user.username}")
							continue

				if User.user.is_premium == True:
					users.append(f"@{User.user.username}")
			readyStore = "\n".join(users)
			print('true');
			print(','.join(users))
		except:
			print('false');
			pass




	if opreat == 'left':
		leaveID   = int(sys.argv[3]);
		leaveID2 = int(sys.argv[4]);

		try:
			await app.leave_chat(leaveID);
			if leaveID != leaveID2:
				await app.leave_chat(leaveID2);
			print('true');
		except Exception as Error:
			print('false',Error);
			pass
		pass

	


	if opreat == 'getusers':
		groupID   = int(sys.argv[3]);
		groupID2 = int(sys.argv[4]);
		OpreatID   = str(sys.argv[5]);
		
		foundUsers       = [];
		notFountUsers = [];
		jart      = get('continue',None,'database/continue.json');
		try :
			countinue_users = jart.split(',');
		except :
			countinue_users = [];
		
		try:
			getFoundUsers     = app.get_chat_members(groupID2);
			async for foundY in getFoundUsers:

				if foundY.user.username is not None:
					#aaaa = await app.get_users(foundY.user.username)
					#p = aaaa.is_premium
					#if p == True:
					foundUsers.append(foundY.user.username);
				else:
					if foundY.user.phone_number is not None:
						foundUsers.append(foundY.user.phone_number);
				pass

			getNotFoundUsers = app.get_chat_members(groupID);
			async for foundN in getNotFoundUsers:

				if foundN.user.username is not None:
					q = await app.get_users(foundN.user.username)
					l = q.is_premium
					if foundN.user.username not in foundUsers and l == True:
						notFountUsers.append(f"@{foundN.user.username}");
						continue;
				
				if foundN.user.phone_number is not None:
					if foundN.user.phone_number not in foundUsers and foundN.user.phone_number not in countinue_users:
						notFountUsers.append(f"+{foundN.user.phone_number}");
			
			readyStore    = "\n".join(notFountUsers);
			#storedMembers(OpreatID,readyStore);
			print('true');
			print(','.join(notFountUsers));
		except:
			print('false');
			pass
	
	
	
	if opreat == 'MovePro':
		
		ToChat      = int(sys.argv[4]); #"TestMovePro"; #toGroupID
		UNChat      = int(sys.argv[3]); #"phpmm"; #fromGroupID
		
		FoundedUsers   = [];
		try:
			GetUsers      = app.get_chat_members(ToChat);
			async for foundedQ in GetUsers:
				if foundedQ.user.id is not None:
					FoundedUsers.append(foundedQ.user.id);
		except Exception as Aroz:
			print('false');
			print('inGetGroupOldMembers!');
			print(Aroz);
		
		if len(sys.argv) > 5:
			AddedReq = int(sys.argv[5]) + 5;
		else:
			AddedReq = 1000 + 5;
			
		IDsUsers    = [];
		ListUsers   = [];
		SuccessUsers = '';
		AddedCount   = 0;
		try:
			async for message in app.get_chat_history(UNChat):
				if AddedCount >= AddedReq:
					print(f"Added {AddedReq} !!");
					break;
				
				if message.from_user is None:
					continue;
				if message.from_user.id is None:
					continue;
				if message.from_user.id in FoundedUsers:
					continue;
				if message.from_user.id in IDsUsers:
					continue;
				
				if message.from_user.id not in IDsUsers:
					try:
						aa = await app.get_users(message.from_user.id)
						d = aa.is_premium
						if d == True:
							IDsUsers.append(message.from_user.id);
					except Exception as ee:
						print(ee)
				if message.from_user.username is not None:
					try:
						aaa = await app.get_users(message.from_user.username)
						f = aaa.is_premium
						if f == True:
							ListUsers.append(f"@{message.from_user.username}")
							#SuccessUsers     += str(message.from_user.username)+',';
							AddedCount     += 1;
					except Exception as ae:
						print(ae)
				elif message.from_user.phone_number is not None:
					ListUsers.append(f"+{message.from_user.phone_number}")
					#SuccessUsers     += str(message.from_user.phone_number)+',';
					AddedCount     += 1;
			print('true');
			print(','.join(ListUsers));
		except Exception as Arooz:
			print('false');
			print(Arooz);
			print('inNewGroupFetchMembers!');
	
	
	if opreat == 'getUsers':
		groupID	= int(sys.argv[3]);
		groupUsers  = [];
		xxz = 0;
		try:
			#getUser     = app.get_chat_members(groupID);
			#async with app:
			async for user in app.iter_chat_members(groupID):
				xxz += 1;
				if xxz >= 1000:
					xxz = 0;
						#time.sleep(5);
					print("Soor "+str(len(groupUsers)));
				if user.user.id is not None:
					groupUsers.append(f"@{user.user.id}");
				else:
					if user.user.phone_number is not None:
						groupUsers.append(f"+{user.user.phone_number}");
				#pass
			#print('true');
			#print(','.join(groupUsers));
			#set("now","mem",','.join(groupUsers));
		except Exception as hhg:
			print('false');
			print(hhg);
			pass
		print(len(groupUsers));

	if opreat == 'adduser':
		groupID	= int(sys.argv[3]);
		userID	   = sys.argv[4];
		OPID          = str(sys.argv[5]);
		pid             = '';
		#jart            = get('continue',None,'database/continue.json');
		
		invited      = get(OPID,None,'database/continue.json');
		
		try :
			inviteds     = invited.split(',');
		except :
			inviteds      = [];
		
		#try :
			#countinue_users = jart.split(',');
		#except :
			#countinue_users = [];
		#await app.send_message(groupID,'Hi guys');
		try :
			#checking     = await app.get_chat_member(
				#chat_id=groupID,
				#user_id=str(userID)
			#)
			#print(checking);
			commoned   = await app.get_common_chats(str(userID));
			#print(commoned);
			for chj in commoned :
				if groupID == chj.id :
					pid    = 'found';
					break;
			
			#if checking.is_member is not None :
				#if checking.is_member == True :
					#pid    = 'found';
		except Exception as w :
			print('continue');
			print('sad',w);
			exit();
			
		if pid    == 'found':
			if userID in inviteds :
				print('true');
				print('From_Inviteds');
				exit();
			else :
				print('continue');
				print('found');
				exit();
		
		try:
			await app.add_chat_members(groupID,str(userID));
			
			pid = 'check';
			
			#if checking.is_member is not None :
				#if checking.is_member is True :
					#print('true');
				#else :
					#print('continue');
					#print('invite');
			#else :
				#print('continue');
				#print('invite');
	
		except FloodWait as Error:
			print('flood');
			print(ses);
		except PeerFlood as Error:
			print('floodANDcontinue');
			print(ses);
		except UserPrivacyRestricted as Error:
			#countinue_users.append(str(userID));
			#set('continue',str(','.join(countinue_users)),None,'database/continue.json');
			print('continue');
			#print(countinue_users);
		except UserNotMutualContact as Error:
			#countinue_users.append(str(userID));
			#set('continue',str(','.join(countinue_users)),None,'database/continue.json');
			print('continue');
			#print(countinue_users);
		except UserChannelsTooMuch as Error:
			#countinue_users.append(str(userID));
			#set('continue',str(','.join(countinue_users)),None,'database/continue.json');
			print('continue');
			#print(countinue_users);
		except Exception as Errors:
			print('continues',groupID,userID,Errors);
		pass
		
		try :
			commoneds   = await app.get_common_chats(str(userID));
			#print(commoneds);
			for chj in commoneds :
				if groupID == chj.id :
					pid    = 'added';
					break;
			if pid == 'added':
				print('true');
			else :
				print('flood');
				print('invite');
				inviteds.append(str(userID));
				set(OPID,str(','.join(inviteds)),None,'database/continue.json');
		except Exception as df:
			print('exz',df);
	
	if opreat == 'addusers':
		groupID	= int(sys.argv[3]);
		userID	   = sys.argv[4];
		UsersIDs   = userID.split(',');
		try:
			await app.add_chat_members(chat_id=groupID, user_ids=UsersIDs,forward_limit=50);
			print('true');
		except Exception as Rddf:
			print('except');
			print(Rddf)
			pass
	
	if opreat == 'AddUser':
		groupID	= int(sys.argv[3]);
		userID	   = sys.argv[4];
		ghj = utils.resolve_username(userID);
		#inpuy         = await app.resolve_peer(groupID);
		try :
			app.invoke(functions.messages.AddChatUser(
				chat_id=groupID,
				user_id=types.InputUser(user_id=ghj,access_hash=0),
				fwd_limit=2
			))
			print('true');
		except FloodWait as Error:
			print('flood');
			print(ses);
		except PeerFlood as Error:
			print('floodANDcontinue');
			print(ses);
		except UserPrivacyRestricted as Error:
			countinue_users.append(str(userID));
			set('continue',str(','.join(countinue_users)),None,'database/continue.json');
			print('continue');
			#print(countinue_users);
		except UserNotMutualContact as Error:
			countinue_users.append(str(userID));
			set('continue',str(','.join(countinue_users)),None,'database/continue.json');
			print('continue');
			#print(countinue_users);
		except UserChannelsTooMuch as Error:
			countinue_users.append(str(userID));
			set('continue',str(','.join(countinue_users)),None,'database/continue.json');
			print('continue');
			#print(countinue_users);
		except Exception as Errors:
			print('continues',groupID,userID,Errors);
		pass
	
	if opreat == 'View':
		chID    = str(sys.argv[3]);
		mgID   = int(sys.argv[4]);
		awr    = await app.resolve_peer(chID),
		rdd     = await app.invoke(
			functions.messages.GetMessagesViews(
				peer=await app.resolve_peer(chID),
				id=[mgID],
				increment=True
			)
		)


	if opreat == 'reaction':
		CHID = str(sys.argv[3])
		MSID = int(sys.argv[4])
		U = str(sys.argv[5])
		await app.send_reaction(CHID, MSID, U)
		


	if opreat == 'Poll':
		CHID = str(sys.argv[3])
		MSID = int(sys.argv[4])
		U = int(sys.argv[5])
		await app.vote_poll(CHID, MSID, U)


	if opreat == 'copy':
		Chat_id = int('777000');
		ID = int('1')
		owner = sys.argv[5]


		a = await app.copy_message(chat_id=Chat_id, from_chat_id=Chat_id, message_id=ID)
		sendMessage(owner,a)
		#i = a.


	if opreat == 'Report':
		chat = sys.argv[4]

		m = await app.get_users(chat)
		print(m)


	
	if opreat == 'send':
		senderID	= sys.argv[3];
		messageID   = sys.argv[4];
		recivedID       = sys.argv[5];
		try:
			await app.copy_message(recivedID,senderID,messageID);
			print('true');
		except FloodWait as Error:
			print('flood');
		except UserRestricted as Error:
			print('continue');
		except PeerFlood as Error:
			print('flood');
		except Exception as Errors:
			print(Errors,'all');
		pass

	if opreat == 'Get':
		Num = sys.argv[2]
		owner = sys.argv[3]
		try:
			random_file = random.choice(sessions)
			num = Client(f"{random_file}",api_id=api_id, api_hash=api_hash)
			Con = num.get_me()
			B = num.session_string
			A = num.phone_number
			set(owner,'owner', owner, 'database/mover.json');
			set(owner,'NUM', A, 'database/mover.json');
			set(owner,'file', random_file, 'database/mover.json')
			set(owner,'sessions', str(B), 'database/mover.json');
			#setownerD,'sess', num, 'database/mover.json');
			set(owner, 'status', 'get', 'database/mover.json')
			return
		except Exception as e:
			sendMessage(owner, f" error {e}")
		


	if opreat == 'leavess':
		seee = sys.argv[2]
		try:
			done = 0;bad = 0
			await leave_all_chats(app)
			done += 1
			print(['true'])
		except Exception as e:
				bad += 1
				print(['false', e])	
	
	if opreat == 'joinlist':
		

		opreatID = sys.argv[4];
		listL = sys.argv[3];
		owner = sys.argv[5];
		LID = sys.argv[6];
		SEL = sys.argv[2];
		#apps = sys.argv[2]
		#apps = SEL


		try:
			done = 0;bad = 0
			SEEE = cSessions

			await join_chatlist(app,listL)
			done += 1
			print(['true'])
		except Exception as e:
				bad += 1
				print(['false', e])
		except:
			TEXT = "- حدث خطا اثناء الدخول الى المجلد ❗"
			sendMessage(owner,TEXT)
			pass
				
				
	if opreat == 'leavelist':

		listE = sys.argv[3];
		opreatID = sys.argv[4];
		owner = sys.argv[5];
		SED = sys.argv[2];


		try:
			done = 0;
			bad = 0;
			await leave_chatlist(app,listE)
			done += 1
			print(['true'])
		except Exception as e:
			bad += 1
			print(['false', e])
			#db.update({'done': DONE}, query.opreatID == 'JoinList')
		except:
			TEXT = "- حدث خطا اثناء الخروج من المجلد ❗"
			sendMessage(owner,TEXT)
			pass

	if opreat == 'joining':
		username     = sys.argv[3];
		try:
			join_to_username    = await app.join_chat(username);
			joining_id                    = join_to_username.id;
			print(['true',joining_id]);
		except Exception as prim:
			print(['false',prim]);
		pass
			
	if opreat == 'CX':
		
		UNChat     = "phpmm"
		IDsUsers    = [];
		ListUsers   = [];
		
		async for message in app.get_chat_history(UNChat):
			if message.from_user.id not in IDsUsers:
				IDsUsers.append(message.from_user.id);
				if message.from_user.username is not None:
					ListUsers.append(message.from_user.username)
				elif message.from_user.phone_number is not None:
					ListUsers.append(message.from_user.phone_number)
		print("Useranames\n\n");
		print(ListUsers);

asyncio.get_event_loop().run_until_complete(Controll());


uvloop.install()
