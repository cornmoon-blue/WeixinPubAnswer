#-*- encoding: utf-8 -*-
import sys, string
import poplib,email

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def fetch_report_from_Email(msg_subject):
    #固定从170邮箱取信息，参数对应不同类型信息内容。返回值为信息字符串
    host = "pop3.sina.com"  # pop3服务器地址
    username = "username@sina.cn"  # 用户名
    password = "xxxx"  # 密码
    pop = poplib.POP3(host)  # 创建一个pop3对象，这个时候实际上已经连接上服务器了
    #pp.set_debuglevel(1) # 设置调试模式，可以看到与服务器的交互信息

    pop.user(username)  # 向服务器发送用户名
    pop.pass_(password)  # 向服务器发送密码
    num,total_size = pop.stat()  # 获取服务器上信件信息，返回是一个列表，第一项是一共有多上封邮件，第二项是共有多少字节
    for i in range(num,(0 if num-10<0 else num-10),-1):  #取最近的5封邮件，注意这里对流量的影响
        hdr,text,octet=pop.retr(i) #取第i封邮件
        text = '\n'.join(text) #将list拼接成字串
        amail = email.message_from_string(text)
        msg = email.message_from_string(text)
        subject = msg.get("subject")  #获得邮件主题
        #subject=msg['subject']  #另一种方法
        #from_user = amail.get("from")  #获得发件人
        if subject.lower()==msg_subject:
            payload=str(msg.get_payload())  #获得邮件内容
            warnning_msg='\r\n注意：以上结果仅供参考，不构成投资建议！'
            payload += warnning_msg
            pop.quit()  # 退出邮箱
            return payload
    pop.quit()  # 退出邮箱
    return '没有新的筛选结果！'  #如果在最新六封邮件没有找到所需主题，则返回提示

def mail_send_message(mail_subject,message_text):
    #参数：邮件主题，消息内容
	#text = analysis_text.decode('utf8')
	smtpserver = 'smtp.sina.com'  #邮件服务器
	username = 'xxxx@sina.cn'  #邮件账号
	password = 'xxxx'   #邮件密码

	from_addr = 'xxxx@sina.cn'   #发件人
	to_addr = 'xxxx@sina.cn'     #收件人
	#send_time = email.utils.formatdate(time.time(),True)
	send_time = time.strftime('%Y-%m-%d %H:%M:%S')  #时间戳

	message = Message()   #实例化
	message['Subject'] = mail_subject   #邮件主题
	message['From'] = from_addr  #发件人
	message['To'] = to_addr  #收件人
	message.set_payload(message_text+'\n'+send_time)  #设置邮件内容
	msg = message.as_string()

	sm = smtplib.SMTP(smtpserver,port=25,timeout=20)  #链接邮件服务器
	#sm.set_debuglevel(1)
	try:
		sm.ehlo()
		sm.starttls()
		sm.ehlo()
		sm.login(username, password)
		sm.sendmail(from_addr, to_addr, msg)
		sleep(2)
		sm.quit()
		return 'mail send completed!'
	except Exception as e:
		return e