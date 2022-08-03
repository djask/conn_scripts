#!/usr/bin/env python3

import os
import sys
import uuid

class crt_format:
  def __init__(self, filename, protocol, hostname, port):
    self.filename = filename
    self.protocol = protocol
    self.hostname = hostname
    self.port = port
    self.name = self.filename.split('/')[-1].replace('.ini', '').replace('.', '-')
    print('name', self.name)

  def get_filename(self):
    return self.filename

  def get_protocol(self):
    return self.protocol

  def get_hostname(self):
    return self.hostname

  def get_port(self):
    return self.port

  def get_name(self):
    return self.name

class crt_folder:
  def __init__(self, path: str):
    self.path = '/'.join(path.split('/')[0:-1])
    self.children = []
    self.root = self.path.split('/')[0]
    self.levels = len(self.path.split('/'))

  def get_path(self):
    return self.path

  def get_root(self):
    return self.root

  def add_child(self, child: crt_format):
    self.children.append(child)

  def get_children(self):
    return self.children

class crt_to_remote:
  def __init__(self, path):
    self.path = path
    self.folders = []
    self._scrape()

  def _parse_file(self, filename):
    """
    Parses a .ini file and converts it into a crt_format object
    """
    with open(filename, 'r') as f:
      lines = f.readlines()
      flag = 0
      valid = 1
      host = ""
      port = 22
      prot = "Unknown"
      for line in lines:
        if 'S:"Protocol Name"' in line:
          prot = line.split('=')[1].strip('\n')
        if 'S:"Hostname"' in line:
          host = line.split('=')[1].strip('\n')
          flag += 1
        elif 'D:"Port"' in line:
          port = int("0x" + line.split('=')[1].strip('\n'), 0)
          flag += 1
        if flag == 2:
          break
      return crt_format(filename, prot, host, port)

  def _scrape(self):
    """
    Iterate each file in the directory given and extract information into the crt_format class
    """
    for path, subdirs, files in os.walk(self.path):
      for name in files:
        if "__FolderData__" in name:
          continue
        full_path = os.path.join(path, name)
        folder = crt_folder(full_path)
        exists = False

        parsed = self._parse_file(full_path)

        for i in self.folders:
          if i.get_path() == folder.get_path():
            exists = True
            i.add_child(parsed)
            break

        if not exists:
          folder.add_child(parsed)
          self.folders.append(folder)

  def generate_id(self) -> str:
    random_id = uuid.uuid4()
    return str(random_id)

  def export_csv(self, export_file: str) -> None:
    """
    Export the data to a CSV file
    """
    with open(export_file, 'w+') as f:
      for i in self.folders:
        for j in i.get_children():
            # remove the .ini from the filename
            short_filename = j.get_filename().split('.')[0]
            f.write(
                short_filename + ',' + 
                j.get_protocol() + ',' + 
                j.get_hostname() + ',' + 
                str(j.get_port()) + '\n'
            )

  def export_xml(self, export_file):
    """
    Export the data to an XML file
    TODO: Populate data and use the correct templates
    """

    header = """<?xml version="1.0" encoding="utf-8"?>
    <mrng:Connections xmlns:mrng="http://mremoteng.org" Name="Connections" Export="false" EncryptionEngine="AES" BlockCipherMode="GCM" KdfIterations="10000" FullFileEncryption="false" Protected="+rESUBQUT6aqqB0Im/8gxpL5gK7uG4bneapzDC+v3t/i0TWEqVBgVdVV1U3CoBd8B7ulXKr2J6hsNnqV694CH6PM" ConfVersion="2.7">\n"""

    # spacing, name, id, hostname, protocol, port
    node_template = """%s<Node Name="%s" VmId="" UseVmId="false" UseEnhancedMode="false" Type="Connection" Descr="" Icon="mRemoteNG" Panel="General" Id="%s" Username="" Domain="" Password="" Hostname="%s" Protocol="%s" RdpVersion="rdc6" SSHTunnelConnectionName="" SSHOptions="" PuttySession="Default Settings" Port="%s" ConnectToConsole="false" UseCredSsp="true" RenderingEngine="IE" RDPAuthenticationLevel="NoAuth" RDPMinutesToIdleTimeout="0" RDPAlertIdleTimeout="false" LoadBalanceInfo="" Colors="Colors16Bit" Resolution="FitToWindow" AutomaticResize="true" DisplayWallpaper="false" DisplayThemes="false" EnableFontSmoothing="false" EnableDesktopComposition="false" DisableFullWindowDrag="false" DisableMenuAnimations="false" DisableCursorShadow="false" DisableCursorBlinking="false" CacheBitmaps="false" RedirectDiskDrives="false" RedirectPorts="false" RedirectPrinters="false" RedirectClipboard="false" RedirectSmartCards="false" RedirectSound="DoNotPlay" SoundQuality="Dynamic" RedirectAudioCapture="false" RedirectKeys="false" Connected="false" PreExtApp="" PostExtApp="" MacAddress="" UserField="" Favorite="false" ExtApp="" StartProgram="" VNCCompression="CompNone" VNCEncoding="EncHextile" VNCAuthMode="AuthVNC" VNCProxyType="ProxyNone" VNCProxyIP="" VNCProxyPort="0" VNCProxyUsername="" VNCProxyPassword="" VNCColors="ColNormal" VNCSmartSizeMode="SmartSAspect" VNCViewOnly="false" RDGatewayUsageMethod="Never" RDGatewayHostname="" RDGatewayUseConnectionCredentials="Yes" RDGatewayUsername="" RDGatewayPassword="" RDGatewayDomain="" />\n"""

    # spacing, name, id
    folder_template = """%s<Node Name="%s" Type="Container" Expanded="true" Descr="" Icon="mRemoteNG" Panel="General" Id="%s" Username="" Domain="" Password="" Hostname="" Protocol="RDP" PuttySession="Default Settings" Port="3389" ConnectToConsole="false" UseCredSsp="true" RenderingEngine="IE" ICAEncryptionStrength="EncrBasic" RDPAuthenticationLevel="NoAuth" RDPMinutesToIdleTimeout="0" RDPAlertIdleTimeout="false" LoadBalanceInfo="" Colors="Colors16Bit" Resolution="FitToWindow" AutomaticResize="true" DisplayWallpaper="false" DisplayThemes="false" EnableFontSmoothing="false" EnableDesktopComposition="false" CacheBitmaps="false" RedirectDiskDrives="false" RedirectPorts="false" RedirectPrinters="false" RedirectSmartCards="false" RedirectSound="DoNotPlay" SoundQuality="Dynamic" RedirectKeys="false" Connected="false" PreExtApp="" PostExtApp="" MacAddress="" UserField="" ExtApp="" VNCCompression="CompNone" VNCEncoding="EncHextile" VNCAuthMode="AuthVNC" VNCProxyType="ProxyNone" VNCProxyIP="" VNCProxyPort="0" VNCProxyUsername="" VNCProxyPassword="" VNCColors="ColNormal" VNCSmartSizeMode="SmartSAspect" VNCViewOnly="false" RDGatewayUsageMethod="Never" RDGatewayHostname="" RDGatewayUseConnectionCredentials="Yes" RDGatewayUsername="" RDGatewayPassword="" RDGatewayDomain="" InheritCacheBitmaps="false" InheritColors="false" InheritDescription="false" InheritDisplayThemes="false" InheritDisplayWallpaper="false" InheritEnableFontSmoothing="false" InheritEnableDesktopComposition="false" InheritDomain="false" InheritIcon="false" InheritPanel="false" InheritPassword="false" InheritPort="false" InheritProtocol="false" InheritPuttySession="false" InheritRedirectDiskDrives="false" InheritRedirectKeys="false" InheritRedirectPorts="false" InheritRedirectPrinters="false" InheritRedirectSmartCards="false" InheritRedirectSound="false" InheritSoundQuality="false" InheritResolution="false" InheritAutomaticResize="false" InheritUseConsoleSession="false" InheritUseCredSsp="false" InheritRenderingEngine="false" InheritUsername="false" InheritICAEncryptionStrength="false" InheritRDPAuthenticationLevel="false" InheritRDPMinutesToIdleTimeout="false" InheritRDPAlertIdleTimeout="false" InheritLoadBalanceInfo="false" InheritPreExtApp="false" InheritPostExtApp="false" InheritMacAddress="false" InheritUserField="false" InheritExtApp="false" InheritVNCCompression="false" InheritVNCEncoding="false" InheritVNCAuthMode="false" InheritVNCProxyType="false" InheritVNCProxyIP="false" InheritVNCProxyPort="false" InheritVNCProxyUsername="false" InheritVNCProxyPassword="false" InheritVNCColors="false" InheritVNCSmartSizeMode="false" InheritVNCViewOnly="false" InheritRDGatewayUsageMethod="false" InheritRDGatewayHostname="false" InheritRDGatewayUseConnectionCredentials="false" InheritRDGatewayUsername="false" InheritRDGatewayPassword="false" InheritRDGatewayDomain="false">\n"""

    node_end = "%s</Node>\n"

    footer = """</mrng:Connections>\n"""


    with open(export_file, 'w') as f:
      f.write(header)
      last_file = ""
      tag_stack = []
      for path, subdirs, files in os.walk(self.path):
        print(path)
        current_name = path.split('/')[-1]
        current_depth = len(path.split('/'))
        last_name = last_file.split('/')[-1]
        last_depth = len(last_file.split('/'))

        if len(current_name) == 0: # root dir
          current_name = path.split('/')[0]

        if len(last_name) == 0:
          last_name = last_file.split('/')[0]
          last_depth = 1

        current_files = []

        current_name = current_name.replace('.', '-')
        last_name = last_name.replace('.', '-')

        for i in files:
          full_path = os.path.join(path, i)

          if "__FolderData__" in full_path:
            continue

          if full_path.endswith(".ini"):
            parsed = self._parse_file(full_path)
            current_files.append(parsed)

        if current_depth >= 2 and last_depth >= 2:
          has_case = False
          current_parent = path.split('/')[-2]
          last_parent = last_file.split('/')[-2]

          if current_depth == last_depth and current_name != last_name: # directory change
            f.write(node_end % (' ' * len(tag_stack)))
            tag_stack.pop()

            tag_stack.append(current_name)
            # f.write('%s<Node name=%s>\n' % (' ' * len(tag_stack), current_name))
            f.write(folder_template % (' ' * len(tag_stack), current_name, self.generate_id()))

            for i in current_files:
              # f.write('%s<Node name=%s />\n' % (' ' * (len(tag_stack) + 1), i.get_name()))
              # name, id, hostname, protocol, port
              f.write(node_template % (' ' * (len(tag_stack) + 1), i.get_name(), self.generate_id(), i.get_hostname(), i.get_protocol(), i.get_port()))
              pass

            has_case = True

          if current_parent != last_parent and current_depth < last_depth: # we are moving back then entering a new directory
            has_case = True
            while len(tag_stack) > 0 and tag_stack[-1] != current_parent:
              f.write(node_end % (' ' * len(tag_stack)))
              tag_stack.pop()
            tag_stack.append(current_name)

            # f.write('%s<Node name=%s>\n' % (' ' * len(tag_stack), current_name))
            f.write(folder_template % (' ' * len(tag_stack), current_name, self.generate_id()))
            for i in current_files:
              #f.write('%s<Node name=%s />\n' % (' ' * (len(tag_stack) + 1), i.get_name()))
              f.write(node_template % (' ' * (len(tag_stack) + 1), i.get_name(), self.generate_id(), i.get_hostname(), i.get_protocol(), i.get_port()))

          if not has_case:
            tag_stack.append(current_name)

            #f.write('%s<Node name=%s>\n' % (' ' * len(tag_stack), current_name))
            f.write(folder_template % (' ' * len(tag_stack), current_name, self.generate_id()))
            for i in current_files:
              # f.write('%s<Node name=%s />\n' % (' ' * (len(tag_stack) + 1), i.get_name()))
              f.write(node_template % (' ' * (len(tag_stack) + 1), i.get_name(), self.generate_id(), i.get_hostname(), i.get_protocol(), i.get_port()))

        elif current_depth == 2 and last_depth == 1:
          tag_stack.append(current_name)
          # f.write('%s<Node name=%s>\n' % (' ' * len(tag_stack), current_name))

          stack_size = ' ' * len(tag_stack)
          # print(type(stack_size), type(current_name), type(self.generate_id()))

          f.write(folder_template % (' ' * len(tag_stack), current_name, self.generate_id()))
          for i in current_files:
            #f.write('%s<Node name=%s />\n' % (' ' * (len(tag_stack) + 1), i.get_name()))
            f.write(node_template % (' ' * (len(tag_stack) + 1), i.get_name(), self.generate_id(), i.get_hostname(), i.get_protocol(), i.get_port()))

        #print('s:', tag_stack)
        last_file = path

      for i in range(len(tag_stack)):
        f.write(node_end % (' ' * len(tag_stack)))
        tag_stack.pop()

      f.write(footer)
      

def main():
  if len(sys.argv) < 3:
    print("Usage: crt_to_remote.py <base folder> <export name>")
    sys.exit(1)

  base_folder = sys.argv[1]
  export_name = sys.argv[2]

  scraper = crt_to_remote(base_folder)
  scraper.export_xml(export_name)

if __name__ == "__main__":
  main()

