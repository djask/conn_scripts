from securecrt_scraper import scrt_scrape
import sys



MREMOTE_HEADER = """<?xml version="1.0" encoding="utf-8"?>
<mrng:Connections xmlns:mrng="http://mremoteng.org" Name="Connections" Export="false" EncryptionEngine="AES" BlockCipherMode="GCM" KdfIterations="10000" FullFileEncryption="false" Protected="+rESUBQUT6aqqB0Im/8gxpL5gK7uG4bneapzDC+v3t/i0TWEqVBgVdVV1U3CoBd8B7ulXKr2J6hsNnqV694CH6PM" ConfVersion="2.7">"""

#name, host protocol, port
MREMOTE_CONN_LINE = """<Node Name="{}" VmId="" UseVmId="false" UseEnhancedMode="false" Type="Connection" Descr="" Icon="mRemoteNG" Panel="General"  Username="" Domain="" Password="" Hostname="{}" Protocol="{}" RdpVersion="rdc6" SSHTunnelConnectionName="" SSHOptions="" PuttySession="Default Settings" Port="{}" ConnectToConsole="false" UseCredSsp="true" RenderingEngine="IE" RDPAuthenticationLevel="NoAuth" RDPMinutesToIdleTimeout="0" RDPAlertIdleTimeout="false" LoadBalanceInfo="" Colors="Colors16Bit" Resolution="FitToWindow" AutomaticResize="true" DisplayWallpaper="false" DisplayThemes="false" EnableFontSmoothing="false" EnableDesktopComposition="false" DisableFullWindowDrag="false" DisableMenuAnimations="false" DisableCursorShadow="false" DisableCursorBlinking="false" CacheBitmaps="false" RedirectDiskDrives="false" RedirectPorts="false" RedirectPrinters="false" RedirectClipboard="false" RedirectSmartCards="false" RedirectSound="DoNotPlay" SoundQuality="Dynamic" RedirectAudioCapture="false" RedirectKeys="false" Connected="false" PreExtApp="" PostExtApp="" MacAddress="" UserField="" Favorite="false" ExtApp="" StartProgram="" VNCCompression="CompNone" VNCEncoding="EncHextile" VNCAuthMode="AuthVNC" VNCProxyType="ProxyNone" VNCProxyIP="" VNCProxyPort="0" VNCProxyUsername="" VNCProxyPassword="" VNCColors="ColNormal" VNCSmartSizeMode="SmartSAspect" VNCViewOnly="false" RDGatewayUsageMethod="Never" RDGatewayHostname="" RDGatewayUseConnectionCredentials="Yes" RDGatewayUsername="" RDGatewayPassword="" RDGatewayDomain="" />"""
MREMOTE_FOOTER = """</mrng:Connections>"""

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print ("Usage: securecrt_scraper.py [base scrt folder]")
        sys.exit()
    crt = scrt_scrape(sys.argv[1])
    crt.scrape_sessions_recursive()
    
    print (MREMOTE_HEADER)
    for s in crt.sessions:
        print (MREMOTE_CONN_LINE.format(s[0], s[2], s[1], s[3]))
    print (MREMOTE_FOOTER)