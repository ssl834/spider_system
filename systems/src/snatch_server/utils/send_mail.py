from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib,time
class SendEmail(object):
    """发送邮件"""
    def __init__(self):
        self.from_addr= '15158062231@163.com'
        self.password = 's6370sl'
        self.to_addr = ['1910227639@qq.com']
        self.smtp_server = 'smtp.163.com'
    def get_server(self):
        self.server=smtplib.SMTP(self.smtp_server, 25)
        self.server.set_debuglevel(1)
        self.server.login(self.from_addr, self.password)
        return self.server
    def _format_addr(self,s):
        name, addr = parseaddr(s)
        return formataddr((Header(name, 'utf-8').encode(), addr))
    def send_email(self,alarm_type,content):
        msg = MIMEText(content, 'plain', 'utf-8')
        msg['From']= self._format_addr('SpiderSystem <%s>' % self.from_addr)
        msg['To'] = self._format_addr('管理员 <%s>' % self.to_addr)
        msg['Subject'] = Header(alarm_type, 'utf-8').encode()
        server=self.get_server()
        try:
            server.sendmail(self.from_addr, [self.to_addr], msg.as_string())
            server.quit()
        except:
            return "邮件发送失败"
if __name__ == '__main__':
    # 防止被认为是垃圾邮件 可以在接受邮箱设置白名单
    SendEmail().send_email('proxy异常','proxy代理池空')
