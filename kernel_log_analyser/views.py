import json
from django.shortcuts import render
from django.http import HttpResponse
import datetime
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import LabelEncoder
import numpy as np
import joblib
from django.views.decorators.csrf import ensure_csrf_cookie
# from rest_framework.decorators import api_view, renderer_classes

type_map={196: 'systemd: Started',
 2: 'dbus-daemon: [session',
 197: 'systemd: Starting',
 187: 'nautilus: Could',
 7: 'gnome-shell: DING:',
 9: 'gnome-shell: Window',
 10: 'gnome-shell: cr_declaration_parse_list_from_buf:',
 199: 'update-notifier: gtk_widget_get_scale_factor:',
 11: 'gnome-shell: unable',
 189: 'pkexec: pam_unix(polkit-1:session):',
 5: 'gnome-calendar: Failed',
 186: 'nautilus: Connecting',
 4: 'gnome-calculato: search-provider.vala:140:',
 193: 'snap-store: not',
 6: 'gnome-shell: ATK',
 195: 'systemd: Reached',
 200: 'xkbcomp: Errors',
 0: 'Xwayland: Failed',
 191: 'pulseaudio: GetManagedObjects()',
 192: 'snap-store: /etc/PackageKit/Vendor.conf',
 194: 'snapd-desktop-i: All',
 198: 'systemd: Startup',
 166: 'kernel: snd_intel8x0',
 181: 'kernel: vmwgfx',
 94: 'kernel: e1000',
 104: 'kernel: hid-generic',
 175: 'kernel: usb',
 161: 'kernel: sd',
 160: 'kernel: scsi',
 81: 'kernel: ahci',
 148: 'kernel: piix4_smbus',
 150: 'kernel: platform',
 157: 'kernel: rtc_cmos',
 106: 'kernel: hub',
 142: 'kernel: ohci-pci',
 86: 'kernel: ata_piix',
 146: 'kernel: pci',
 147: 'kernel: pci_bus',
 79: 'kernel: acpi',
 3: 'gdm-session-wor: gkr-pam:',
 8: 'gnome-shell: JS',
 1: 'cron: pam_unix(cron:session):',
 188: 'pkexec: jagannath:',
 190: 'pool-org.gnome.: SECCOMP',
 87: 'kernel: audit:',
 156: 'kernel: rfkill:',
 126: 'kernel: loop14:',
 35: 'kernel: IPv6:',
 95: 'kernel: e1000:',
 117: 'kernel: kauditd_printk_skb:',
 158: 'kernel: sched:',
 78: 'kernel: [drm]',
 21: 'kernel: Console:',
 101: 'kernel: fbcon:',
 77: 'kernel: [drm:vmw_host_printf',
 76: 'kernel: [TTM]',
 113: 'kernel: intel_rapl_msr:',
 154: 'kernel: random:',
 179: 'kernel: vboxguest:',
 110: 'kernel: input:',
 178: 'kernel: vbg_heartbeat_init:',
 125: 'kernel: loop13:',
 124: 'kernel: loop12:',
 123: 'kernel: loop11:',
 122: 'kernel: loop10:',
 135: 'kernel: loop9:',
 134: 'kernel: loop8:',
 133: 'kernel: loop7:',
 132: 'kernel: loop6:',
 131: 'kernel: loop5:',
 130: 'kernel: loop4:',
 129: 'kernel: loop3:',
 128: 'kernel: loop2:',
 127: 'kernel: loop1:',
 121: 'kernel: loop0:',
 116: 'kernel: ipmi',
 34: 'kernel: IPMI',
 65: 'kernel: Started',
 152: 'kernel: ppdev:',
 20: 'kernel: Condition',
 28: 'kernel: Finished',
 137: 'kernel: lp:',
 59: 'kernel: Reached',
 14: 'kernel: Activated',
 16: 'kernel: Adding',
 139: 'kernel: modprobe@drm.service:',
 66: 'kernel: Starting',
 15: 'kernel: Activating',
 47: 'kernel: Mounted',
 27: 'kernel: EXT4-fs',
 48: 'kernel: Mounting',
 140: 'kernel: modprobe@fuse.service:',
 138: 'kernel: modprobe@configfs.service:',
 42: 'kernel: Listening',
 64: 'kernel: Set',
 22: 'kernel: Created',
 57: 'kernel: Queued',
 30: 'kernel: Hostname',
 24: 'kernel: Detected',
 169: 'kernel: systemd',
 38: 'kernel: Inserted',
 177: 'kernel: usbhid:',
 176: 'kernel: usbcore:',
 12: 'kernel: ',
 84: 'kernel: ata3.00:',
 85: 'kernel: ata3:',
 105: 'kernel: hid:',
 13: 'kernel: ACPI:',
 60: 'kernel: Run',
 183: 'kernel: x86/mm:',
 29: 'kernel: Freeing',
 75: 'kernel: Write',
 58: 'kernel: RAS:',
 54: 'kernel: PM:',
 100: 'kernel: evm:',
 109: 'kernel: ima:',
 43: 'kernel: Loaded',
 44: 'kernel: Loading',
 17: 'kernel: AppArmor:',
 39: 'kernel: Key',
 185: 'kernel: zswap:',
 88: 'kernel: blacklist:',
 155: 'kernel: registered',
 159: 'kernel: sched_clock:',
 33: 'kernel: IPI',
 49: 'kernel: NET:',
 36: 'kernel: In-situ',
 62: 'kernel: Segment',
 93: 'kernel: drop_monitor:',
 119: 'kernel: ledtrig-cpu:',
 112: 'kernel: intel_pstate:',
 91: 'kernel: device-mapper:',
 107: 'kernel: i2c_dev:',
 141: 'kernel: mousedev:',
 162: 'kernel: serio:',
 108: 'kernel: i8042:',
 174: 'kernel: uhci_hcd:',
 144: 'kernel: ohci-platform:',
 143: 'kernel: ohci-pci:',
 145: 'kernel: ohci_hcd:',
 98: 'kernel: ehci-platform:',
 97: 'kernel: ehci-pci:',
 99: 'kernel: ehci_hcd:',
 73: 'kernel: VFIO',
 55: 'kernel: PPP',
 173: 'kernel: tun:',
 83: 'kernel: ata2:',
 82: 'kernel: ata1:',
 136: 'kernel: loop:',
 41: 'kernel: Linux',
 63: 'kernel: Serial:',
 163: 'kernel: shpchp:',
 114: 'kernel: io',
 19: 'kernel: Block',
 18: 'kernel: Asymmetric',
 111: 'kernel: integrity:',
 102: 'kernel: fuse:',
 168: 'kernel: squashfs:',
 184: 'kernel: zbud:',
 182: 'kernel: workingset:',
 37: 'kernel: Initialise',
 167: 'kernel: software',
 52: 'kernel: PCI-DMA:',
 70: 'kernel: Trying',
 53: 'kernel: PCI:',
 72: 'kernel: UDP-Lite',
 71: 'kernel: UDP',
 45: 'kernel: MPTCP',
 68: 'kernel: TCP:',
 67: 'kernel: TCP',
 170: 'kernel: tcp_listen_portaddr_hash',
 32: 'kernel: IP',
 89: 'kernel: clocksource:',
 151: 'kernel: pnp:',
 74: 'kernel: VFS:',
 96: 'kernel: e820:',
 50: 'kernel: NetLabel:',
 25: 'kernel: EDAC',
 56: 'kernel: PTP',
 153: 'kernel: pps_core:',
 180: 'kernel: vgaarb:',
 120: 'kernel: libata',
 61: 'kernel: SCSI',
 115: 'kernel: iommu:',
 51: 'kernel: PCI',
 31: 'kernel: HugeTLB',
 40: 'kernel: Kprobes',
 80: 'kernel: acpiphp:',
 90: 'kernel: cpuidle:',
 26: 'kernel: EISA',
 171: 'kernel: thermal_sys:',
 23: 'kernel: DMA:',
 149: 'kernel: pinctrl',
 103: 'kernel: futex',
 92: 'kernel: devtmpfs:',
 165: 'kernel: smpboot:',
 164: 'kernel: smp:',
 118: 'kernel: kvm-clock:',
 172: 'kernel: tsc:',
 46: 'kernel: Measured',
 69: 'kernel: TSC'}


def Logistic_regression(request):
    if(request.method == 'POST'):
        print(json.loads(request.body)['msg'])
        msg=json.loads(request.body)['msg']

        le = LabelEncoder()

        with open(r'C:\Users\jagan\Desktop\hpe\kernel_log_analyser\kernel_log_analyser\classes.npy','rb') as label:
            le.classes_ = label
            print(le)
        with open(r'C:\Users\jagan\Desktop\hpe\kernel_log_analyser\kernel_log_analyser\vectorizer.pickle','rb') as vect_pickle:
            cv=joblib.load(vect_pickle)
            print(cv)
        
                
        with open(r'C:\Users\jagan\Desktop\hpe\kernel_log_analyser\kernel_log_analyser\logistic_regression','rb') as f:
            model=pickle.load(f)
            data=[msg]
            vect=cv.transform(data).toarray()
        
        return HttpResponse(type_map[model.predict(vect)[0]])
    return HttpResponse('Make a post request')

def KNeighborsClassifier(request):
    if(request.method == 'POST'):
        print(json.loads(request.body)['msg'])
        msg=json.loads(request.body)['msg']

        le = LabelEncoder()

        with open(r'C:\Users\jagan\Desktop\hpe\kernel_log_analyser\kernel_log_analyser\classes.npy','rb') as label:
            le.classes_ = label
            print(le)
        with open(r'C:\Users\jagan\Desktop\hpe\kernel_log_analyser\kernel_log_analyser\vectorizer.pickle','rb') as vect_pickle:
            cv=joblib.load(vect_pickle)
            print(cv)
        
                
        with open(r'C:\Users\jagan\Desktop\hpe\kernel_log_analyser\kernel_log_analyser\KNeighborsClassifier','rb') as f:
            model=pickle.load(f)
            data=[msg]
            vect=cv.transform(data).toarray()
        
        return HttpResponse(type_map[model.predict(vect)[0]])
    return HttpResponse('Make a post request')

def DecisionTreeClassifier(request):
    if(request.method == 'POST'):
        print(json.loads(request.body)['msg'])
        msg=json.loads(request.body)['msg']

        le = LabelEncoder()

        with open(r'C:\Users\jagan\Desktop\hpe\kernel_log_analyser\kernel_log_analyser\classes.npy','rb') as label:
            le.classes_ = label
            print(le)
        with open(r'C:\Users\jagan\Desktop\hpe\kernel_log_analyser\kernel_log_analyser\vectorizer.pickle','rb') as vect_pickle:
            cv=joblib.load(vect_pickle)
            print(cv)
        
                
        with open(r'C:\Users\jagan\Desktop\hpe\kernel_log_analyser\kernel_log_analyser\Decision_Trees','rb') as f:
            model=pickle.load(f)
            data=[msg]
            vect=cv.transform(data).toarray()
        
        return HttpResponse(type_map[model.predict(vect)[0]])
    return HttpResponse('Make a post request')

def RandomForest(request):
    if(request.method == 'POST'):
        print(json.loads(request.body)['msg'])
        msg=json.loads(request.body)['msg']

        le = LabelEncoder()

        with open(r'C:\Users\jagan\Desktop\hpe\kernel_log_analyser\kernel_log_analyser\classes.npy','rb') as label:
            le.classes_ = label
            print(le)
        with open(r'C:\Users\jagan\Desktop\hpe\kernel_log_analyser\kernel_log_analyser\vectorizer.pickle','rb') as vect_pickle:
            cv=joblib.load(vect_pickle)
            print(cv)
        
                
        with open(r'C:\Users\jagan\Desktop\hpe\kernel_log_analyser\kernel_log_analyser\Random_Forest','rb') as f:
            model=pickle.load(f)
            data=[msg]
            vect=cv.transform(data).toarray()
        
        return HttpResponse(type_map[model.predict(vect)[0]])
    return HttpResponse('Make a post request')

def NaiveBayes(request):
    if(request.method == 'POST'):
        print(json.loads(request.body)['msg'])
        msg=json.loads(request.body)['msg']

        le = LabelEncoder()

        with open(r'C:\Users\jagan\Desktop\hpe\kernel_log_analyser\kernel_log_analyser\classes.npy','rb') as label:
            le.classes_ = label
            print(le)
        with open(r'C:\Users\jagan\Desktop\hpe\kernel_log_analyser\kernel_log_analyser\vectorizer.pickle','rb') as vect_pickle:
            cv=joblib.load(vect_pickle)
            print(cv)
        
                
        with open(r'C:\Users\jagan\Desktop\hpe\kernel_log_analyser\kernel_log_analyser\Naive_Bayes','rb') as f:
            model=pickle.load(f)
            data=[msg]
            vect=cv.transform(data).toarray()
        
        return HttpResponse(type_map[model.predict(vect)[0]])
    return HttpResponse('Make a post request')