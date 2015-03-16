import datetime

class Host(object):
    def __init__(self, dns, id, ip, last_scan, netbios, os, tracking_method):
        self.dns = str(dns)
        self.id = int(id)
        self.ip = str(ip)
        last_scan = str(last_scan).replace('T', ' ').replace('Z', '').split(' ')
        date = last_scan[0].split('-')
        time = last_scan[1].split(':')
        self.last_scan = datetime.datetime(int(date[0]), int(date[1]), int(date[2]), int(time[0]), int(time[1]), int(time[2]))
        self.netbios = str(netbios)
        self.os = str(os)
        self.tracking_method = str(tracking_method)
        
class AssetGroup(object):
    def __init__(self, business_impact, id, last_update, scanips, scanner_appliances, title):
        self.business_impact = str(business_impact)
        self.id = int(id)
        self.last_update = str(last_update)
        self.scanips = scanips
        self.scanner_appliances = scanner_appliances
        self.title = str(title)
        
    def addAsset(conn, ip):
        call = '/api/2.0/fo/asset/group/'
        parameters = {'action': 'edit', 'id': self.id, 'add_ips': ip}
        conn.request(call, parameters)
        self.scanips.append(ip)
        
    def setAssets(conn, ips):
        call = '/api/2.0/fo/asset/group/'
        parameters = {'action': 'edit', 'id': self.id, 'set_ips': ips}
        conn.request(call, parameters)
        
class Scan(object):
    def __init__(self, assetgroups, duration, launch_datetime, option_profile, processed, ref, status, target, title, type, user_login):
        self.assetgroups = assetgroups
        self.duration = str(duration)
        launch_datetime = str(launch_datetime).replace('T', ' ').replace('Z', '').split(' ')
        date = launch_datetime[0].split('-')
        time = launch_datetime[1].split(':')
        self.launch_datetime = datetime.datetime(int(date[0]), int(date[1]), int(date[2]), int(time[0]), int(time[1]), int(time[2]))
        self.option_profile = str(option_profile)
        self.processed = int(processed)
        self.ref = str(ref)
        self.status = str(status.STATE)
        self.target = str(target).split(', ')
        self.title = str(title)
        self.type = str(type)
        self.user_login = str(user_login)
        
    def cancel(conn):
        cancelled_statuses = ['Cancelled', 'Finished', 'Error']
        if any(self.status in s for s in cancelled_statuses):
            raise ValueError("Scan cannot be cancelled because its status is "+self.status)
        else:
            call = '/api/2.0/fo/scan/'
            parameters = {'action': 'cancel', 'scan_ref': self.ref}
            conn.request(call, parameters)
            
            parameters = {'action': 'list', 'scan_ref': self.ref, 'show_status': 1}
            self.status = objectify.fromstring(conn.request(call, parameters)).RESPONSE.SCAN_LIST.SCAN.STATUS.STATE
            
    def pause(conn):
        if self.status != "Running":
            raise ValueError("Scan cannot be paused because its status is "+self.status)
        else:
            call = '/api/2.0/fo/scan/'
            parameters = {'action': 'pause', 'scan_ref': self.ref}
            conn.request(call, parameters)
            
            parameters = {'action': 'list', 'scan_ref': self.ref, 'show_status': 1}
            self.status = objectify.fromstring(conn.request(call, parameters)).RESPONSE.SCAN_LIST.SCAN.STATUS.STATE
            
    def resume(conn):
        if self.status != "Paused":
            raise ValueError("Scan cannot be resumed because its status is "+self.status)
        else
            call = '/api/2.0/fo/scan/'
            parameters = {'action': 'resume', 'scan_ref': self.ref}
            conn.request(call, parameters)
            
            parameters = {'action': 'list', 'scan_ref': self.ref, 'show_status': 1}
            self.status = objectify.fromstring(conn.request(call, parameters)).RESPONSE.SCAN_LIST.SCAN.STATUS.STATE