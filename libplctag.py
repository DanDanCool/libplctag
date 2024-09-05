import jmake

jmake.setupenv()

base_src_path = 'src'
lib_src_path = f"{base_src_path}/lib"
protocol_src_path = f"{base_src_path}/protocols"
ab_src_path = f"{protocol_src_path}/ab"
mb_src_path = f"{protocol_src_path}/mb"
util_src_path = f"{base_src_path}/util"
example_src_path = f"{base_src_path}/examples"
test_src_path = f"{base_src_path}/tests"
cli_src_path = f"{base_src_path}/contrib/cli"
platform_src_path = f"{base_src_path}/platform/windows"

# set up the library sources
files = [
    f"{lib_src_path}/init.c",
    f"{lib_src_path}/init.h",
    f"{lib_src_path}/libplctag.h",
    f"{lib_src_path}/lib.c",
    f"{lib_src_path}/tag.h",
    f"{lib_src_path}/version.h",
    f"{lib_src_path}/version.c",
    f"{ab_src_path}/ab.h",
    f"{ab_src_path}/ab_common.c",
    f"{ab_src_path}/ab_common.h",
    f"{ab_src_path}/cip.c",
    f"{ab_src_path}/cip.h",
    f"{ab_src_path}/defs.h",
    f"{ab_src_path}/eip_cip.c",
    f"{ab_src_path}/eip_cip.h",
    f"{ab_src_path}/eip_cip_special.c",
    f"{ab_src_path}/eip_cip_special.h",
    f"{ab_src_path}/eip_lgx_pccc.c",
    f"{ab_src_path}/eip_lgx_pccc.h",
    f"{ab_src_path}/eip_plc5_dhp.c",
    f"{ab_src_path}/eip_plc5_dhp.h",
    f"{ab_src_path}/eip_plc5_pccc.c",
    f"{ab_src_path}/eip_plc5_pccc.h",
    f"{ab_src_path}/eip_slc_dhp.c",
    f"{ab_src_path}/eip_slc_dhp.h",
    f"{ab_src_path}/eip_slc_pccc.c",
    f"{ab_src_path}/eip_slc_pccc.h",
    f"{ab_src_path}/error_codes.c",
    f"{ab_src_path}/error_codes.h",
    f"{ab_src_path}/pccc.c",
    f"{ab_src_path}/pccc.h",
    f"{ab_src_path}/session.c",
    f"{ab_src_path}/session.h",
    f"{ab_src_path}/tag.h",
    f"{protocol_src_path}/omron/omron.h",
    f"{protocol_src_path}/omron/omron_common.c",
    f"{protocol_src_path}/omron/omron_common.h",
    f"{protocol_src_path}/omron/cip.c",
    f"{protocol_src_path}/omron/cip.h",
    f"{protocol_src_path}/omron/conn.c",
    f"{protocol_src_path}/omron/conn.h",
    f"{protocol_src_path}/omron/defs.h",
    f"{protocol_src_path}/omron/omron_raw_tag.c",
    f"{protocol_src_path}/omron/omron_raw_tag.h",
    f"{protocol_src_path}/omron/omron_standard_tag.c",
    f"{protocol_src_path}/omron/omron_standard_tag.h",
    f"{protocol_src_path}/omron/tag.h",
    f"{mb_src_path}/modbus.c",
    f"{mb_src_path}/modbus.h",
    f"{protocol_src_path}/system/system.c",
    f"{protocol_src_path}/system/system.h",
    f"{protocol_src_path}/system/tag.h",
    f"{util_src_path}/atomic_int.c",
    f"{util_src_path}/atomic_int.h",
    f"{util_src_path}/attr.c",
    f"{util_src_path}/attr.h",
    f"{util_src_path}/byteorder.h",
    f"{util_src_path}/debug.c",
    f"{util_src_path}/debug.h",
    f"{util_src_path}/hash.c",
    f"{util_src_path}/hash.h",
    f"{util_src_path}/hashtable.c",
    f"{util_src_path}/hashtable.h",
    f"{util_src_path}/macros.h",
    f"{util_src_path}/rc.c",
    f"{util_src_path}/rc.h",
    f"{util_src_path}/vector.c",
    f"{util_src_path}/vector.h",
    f"{platform_src_path}/platform.c",
    f"{platform_src_path}/platform.h",
]

cli_files =  [
    f"{cli_src_path}/cli.c",
    f"{cli_src_path}/cli.h",
    f"{cli_src_path}/getline.h",
    f"{cli_src_path}/uthash.h",
    f"{example_src_path}/utils_windows.c",
    f"{util_src_path}/debug.c",
    f"{util_src_path}/debug.h",
    f"{platform_src_path}/platform.c",
    f"{platform_src_path}/platform.h",
]

vermaj = 2
vermin = 6
verpat = 3
version = f"{vermaj}.{vermin}.{verpat}"

env = jmake.Env()
if env.mode == 'generate':
    jmake.configure_file(jmake.fullpath(f"{lib_src_path}/version.h.in")[0], jmake.fullpath(f"{lib_src_path}/version.h")[0], {
        'VERSION': version,
        'libplctag_VERSION_MAJOR': vermaj,
        'libplctag_VERSION_MINOR': vermin,
        'libplctag_VERSION_PATCH': verpat,
        })

workspace = jmake.Workspace('libplctag')
workspace.lang = 'c11'

libplctag = jmake.Project('libplctag', jmake.Target.SHARED_LIBRARY)
libplctag.define('LIBPLCTAGDLL_EXPORTS', 1)

libplctag.add(jmake.fullpath(files))
libplctag.depend('Ws2_32')
libplctag.include(jmake.fullpath([
    base_src_path, lib_src_path, protocol_src_path, ab_src_path, mb_src_path, util_src_path, platform_src_path
    ]))
libplctag.export(includes=jmake.fullpath('src'))

debug = libplctag.filter('debug')
debug['debug'] = True

cli = jmake.Project('cli', jmake.Target.EXECUTABLE)
cli.define('IS_WINDOWS', 1)
cli.add(jmake.fullpath(cli_files))
cli.include(jmake.fullpath([
    base_src_path, lib_src_path, protocol_src_path, ab_src_path, mb_src_path, util_src_path, platform_src_path
    ]))
cli.depend(libplctag)
cli.depend('Ws2_32')

debug = cli.filter('debug')
debug['debug'] = True

workspace.add(libplctag)
workspace.add(cli)
jmake.generate(workspace)
