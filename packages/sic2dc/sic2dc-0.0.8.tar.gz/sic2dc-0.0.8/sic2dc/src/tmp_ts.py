from ruamel.yaml import YAML

from config_compare import sic2dc
from tools import load_yaml

#f1 = "/home/onale/workdir/avd-dh01/tmp_diff/desired_DH01-12c18-BLF-1-A.cfg"
#f2 = "/home/onale/workdir/avd-dh01/tmp_diff/oper_DH01-12c18-BLF-1-A.cfg"

f1 = "/home/onale/workdir/avd-ud/tmp_diff/desired_UD-d05-BLF-1-A.cfg"
f2 = "/home/onale/workdir/avd-ud/tmp_diff/oper_UD-d05-BLF-1-A.cfg"
fs = "/home/onale/workdir/avd-dh01/group_vars/tmp_cc_settings.yml"

fs = load_yaml(fs)

result = sic2dc(f1, f2, fs['cc_settings'], fs['cc_filters'], cures=[], color = True)
print('\n'.join(result['diff_lines']))
pass