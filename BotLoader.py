# -*- coding: utf-8 -*-
import os
import json
import time
from utils.rtext import RAction, RText, RTextList

prefix = '!!bl'
plugin_name = 'MCDR BotLoader 插件'
plugin_version = '3.0'

help_message: str = '''
§r-----{1} v {2}-----
§dBy CalciumSilicate
用于指令生成bot组
§r{0} §7查§7看§7帮§7助§7信§7息
§r{0} make§r §6<配置名字>§r §7新§7建§7一§7个§7配§7置§7文§7件
§r{0} add§r <bot名字> §6<配置名字>§r <X>§r <Y>§r <Z>§r §e[维度]§r §e[模式]§r §e[是否延时删除]§r §7为§7一§7个§7配§7置§7文§7件§7新§7增§7一§7个§7b§7o§7t§7
§r{0} edit§r <bot名字> §6<配置名字>§r <参数名>§r <参数>§r §7修§7改§7一§7个§7配§7置§7文§7件§7的§7b§7o§7t§7的§7参§7数
§r{0} del§r §6<配置名字>§r §7删§7除§7配§7置
§r{0} del_bot§r <bot名字> §r §6<配置名字>§r §7删§7除§7配§7置§7中§7的§7b§7o§7t
§r{0} list§r §7显§7示§7所§7有§7现§7有§7配置
§r{0} details§r §6<配置名字>§r §7显§7示§7一§7个§7配§7置§7的§7内§7容
§r{0} spawn§r §6<配置名字>§r §7生§7成§7配§7置§7中§7的§7所§7有§7b§7o§7t§7 
§r{0} kill§r §6<配置名字>§r §7下§7线§7配§7置§7中§7的§7所§7有§7b§7o§7t
§r{0} gm§r §6<配置名字>§r §e<模式>§r §7修§7改§7配§7置§7中§7所§7有§7b§7o§7t§7的§7游§7戏§7模§7式
§r{0} add_bot§r §r <bot名字> §6<配置名字>§r §e[是否延时删除]§r §7将§7已§7有§7b§7o§7t§7添§7加§7到§7配§7置§7中
§r{0} add_all§r §6<配置名字>§r §7将§7现§7有§7b§7o§7t§7全§7部§7添§7加§7至§7配§7置§7中
§r{0} del_all§r §6<配置名字>§r §7将§7现§7有§7配§7置§7中§7的§7所§7有§7b§7o§7t§7删§7除§7(§7保§7留§7一§7个§7空§7配§7置§7)
§r{0} add_auto§r §6<配置名字>§r §7在§7开§7服§7自§7启§7的§7配§7置§7中§7添§7加
§r{0} del_auto§r §6<配置名字>§r §7在§7开§7服§7自§7启§7的§7配§7置§7中§7删§7除
§r{0} auto_list§r §7查§7看§7开§7服§7自§7启§7的§7列§7表 
§r-----参数说明-----
§r{0} edit§r中的§r <参数名>§r 可以为: §b name§r / §b x§r / §b y§r / §b z§r / §b dimension§r / §b pos§r / §b delay§r / §b gamemode§r (区分大小写)
§7 name - str  §7 x, y, z - int/float  §7 dimension - 0/-1/1 - overworld/the_nether/the_end  §7 pos - x,y,z  §7 delay - bool
§c  pos的格式为§c§b§cX,Y,Z§r§c(半角逗号)而不是§c§b§c X Y Z§r'''.format('§c§l{}§r§b'.format(prefix), plugin_name, plugin_version)
plugin_msg_prefix = '§r[§dBotLoader§r]'
block_list = ['bot', '_b_', 'Steve', 'Alex', 'loader', 'PCRC', 'FX_White']
setting_list = []
detail = {}
bot_exec_gamemode = {}
player_list = []
bot_online_list = []
MCDRpath = r''
# MCDR路径，留空默认
config_folder = 'config'
config_name = 'BotLoader.json'
config_path = os.path.join(MCDRpath, config_folder, config_name)
Delay = 25

if not os.path.exists(config_path):
    with open(config_path, 'w') as configfile:
        configfile.write(json.dumps({'loader': {}, 'auto_list': []}, indent=4))
else:
    with open(config_path, 'r') as configfile:
        config = json.load(configfile)
    try:
        tmp = config['auto_list']
    except KeyError:
        config['auto_list'] = []
        with open(config_path, 'w') as configfile:
            configfile.write(json.dumps(config, indent=4))


def simple_RText(message, text='', command='', action=RAction.run_command):
    text = RText(message).set_hover_text(text).set_click_event(RAction.suggest_command, '')
    if command:
        text.set_click_event(action, command)
        if not text:
            text.set_hover_text(command)
    return text


detailed_params_help_message = {
    '§e[是否延时删除]': simple_RText('§e[是否延时删除]', '§b(可选参数)§r\n输入§bTrue§r或§cFalse§r(不限制大小写)\n控制是否在召唤bot一定时间后踢除bot'
                                             '\n默认时间: 25s', ''
    ),
    '§e[维度]': simple_RText('§e[维度]', '§b(可选参数)§r\n控制bot生成后所在的世界\n'
                                     '§b主世界 §r- §b0 §r-§b overworld\n'
                                     '§c下界  §r- §c-1 §r-§c the_nether\n'
                                     '§5末地  §r- §51  §r-§5 the_end', ''
    ),
    '§e[模式]': simple_RText('§e[模式]', '§b(可选参数)§r\n控制bot生成后的模式\n'
                                     '§a生存 §r- §a0 §r-§a survival\n'
                                     '§b创造 §r- §b1 §r-§b creative\n'
                                     '§c冒险 §r- §c2 §r-§c adventure\n'
                                     '§7旁观 §r- §73 §r-§7 spectator', ''
    ),
    '§r <参数名>': simple_RText('§r <参数名>', '§c(必选参数)§r\n修改控制bot的各种参数\n'
                                         '§ x, y, z §r- 小数或整数\n§7分别控制bot坐标三个参数\n'
                                         '§l dimension§r - 字符串或整数\n§7控制bot生成后所在的世界\n'
                                         '§l delay§r - True / False\n§7控制是否在召唤bot一定时间后踢除bot\n'
                                         '§l gamemode§r - 字符串或整数\n§7控制bot生成后的模式\n'
                                         '§l name§r - 字符串\n§7控制bot的名字\n'
                                         '§l pos§r - 字符串(x,y,z)\n§7同时控制bot坐标三个参数', ''
    ),
    '§r <参数>': simple_RText('§r <参数>', '§c(必选参数)§r\n修改控制bot的各种参数\n'
                                       '§ x, y, z §r- 小数或整数\n§7控制生成坐标\n'
                                       '§l dimension§r:\n'
                                       '§b主世界 §r- §b0 §r-§b overworld\n'
                                       '§c下界  §r- §c-1 §r-§c the_nether\n'
                                       '§5末地  §r- §51  §r-§5 the_end\n§7控制bot生成后所在的世界\n'
                                       '§l delay§r - True / False\n§7控制是否在召唤bot一定时间后踢除bot\n'
                                       '§l gamemode§r:\n'
                                       '§a生存 §r- §a0 §r-§a survival\n'
                                       '§b创造 §r- §b1 §r-§b creative\n'
                                       '§c冒险 §r- §c2 §r-§c adventure\n'
                                       '§7旁观 §r- §73 §r-§7 spectator\n§7控制bot生成后的模式', ''
    ),
    '§e<模式>': simple_RText('§e<模式>', '§c(必选参数)§r\n控制bot生成后的模式\n'
                                     '§a生存 §r- §a0 §r-§a survival\n'
                                     '§b创造 §r- §b1 §r-§b creative\n'
                                     '§c冒险 §r- §c2 §r-§c adventure\n'
                                     '§7旁观 §r- §73 §r-§7 spectator', ''
    ),
    '§r <bot名字> ': simple_RText('§r <bot名字> ', '§c(必选参数)§r\n控制bot的名字', ''
    ),
    '§r <X>': simple_RText('§r <X>', '§c(必选参数)§r\n控制bot的X坐标', ''),
    '§r <Y>': simple_RText('§r <Y>', '§c(必选参数)§r\n控制bot的Y坐标', ''),
    '§r <Z>': simple_RText('§r <Z>', '§c(必选参数)§r\n控制bot的Z坐标', ''),
    '§6<配置名字>': simple_RText('§6<配置名字>', '§c(必选参数)§r\n点击输入命令\n{} list查看现有配置列表'.format(prefix),
        '{} list'.format(prefix)
    )
}


class Cls:
    is_player = False


class Called:
    content = None
    is_called = True
    is_player = False


def pt_message(server, info, msg, tell=True, print_prefix=''):
    msg = print_prefix + msg
    if info.is_player and not tell:
        server.say(msg)
    else:
        server.reply(info, msg)


def str2bool(arg: str, default: bool or None = True) -> bool or None:
    try:
        if isinstance(eval(arg.title()), bool):
            return eval(arg.title())
    except SyntaxError:
        if default is None:
            return None
    return default


def is_bot(name):
    flag = False
    for block_key in block_list:
        if name.upper().find(block_key.upper()) != -1:
            flag = True
            break
    return flag


def write_in(config_dict):
    with open(config_path, 'w') as config_file:
        config_file.write(json.dumps(config_dict, sort_keys=False, indent=4, separators=(',', ': ')))


def read():
    with open(config_path, 'r') as config_file:
        return json.load(config_file)


def print_message(server, info, msg, is_tell=True, msg_prefix=''):
    if not isinstance(msg, RTextList):
        for line in msg.splitlines():
            if info.is_player:
                if is_tell:
                    server.tell(info.player, f'{msg_prefix}{line}')
                else:
                    server.say(f'{msg_prefix}{line}')
            else:
                server.reply(info, f'{msg_prefix}{line}')
    else:
        if info.is_player:
            if is_tell:
                server.tell(info.player, f'{msg_prefix}{msg}')
            else:
                server.say(f'{msg_prefix}{msg}')
        else:
            server.reply(info, f'{msg_prefix}{msg}')


def print_plugin_message(server, info, msg, is_tell=True):
    print_message(server, info, msg, is_tell, plugin_msg_prefix)


def new_setting(server, info, new_setting_name):
    global config
    if new_setting_name not in setting_list:
        config['loader'][new_setting_name] = {'botlist': {}, 'delay': True}
        print_plugin_message(server, info, '成功创建名为{}的配置'.format(new_setting_name))
    else:
        print_plugin_message(server, info, '已存在名为{}的配置'.format(new_setting_name))


def add_bot_to_setting(
        server,
        info,
        bot_name,
        setting_name,
        X, Y, Z,
        dimension: str or int = 'overworld',
        gamemode='creative',
        delay: str or int or bool = 'global'
):
    global config
    if setting_name not in setting_list:
        print_plugin_message(server, info, '不存在名为{}的配置'.format(setting_name))
        return
    if bot_name in list(config['loader'][setting_name]['botlist'].keys()):
        print_plugin_message(server, info, '在{}中已存在名为{}的bot'.format(setting_name, bot_name))
        return
    if delay is None:
        delay = config['loader'][setting_name]['delay']
    dimension_dict = {-1: 'the_nether', 0: 'overworld', 1: 'the_end'}
    if dimension in list(dimension_dict.keys()):
        dimension = dimension_dict[int(dimension)]
    gamemode_dict = {0: 'survival', 1: 'creative', 2: 'adventure', 3: 'spectator'}
    if gamemode in list(gamemode_dict.keys()):
        gamemode = gamemode_dict[int(gamemode)]
    if dimension not in list(dimension_dict.values()):
        print_plugin_message(server, info,
            '不存在名为{}的维度'.format(dimension))
    if gamemode not in list(gamemode_dict.values()):
        print_plugin_message(server, info, '不存在名为{}的模式'.format(gamemode))
    config['loader'][setting_name]['botlist'][bot_name] = {'x': X, 'y': Y, 'z': Z,
        'dimension': '{}:{}'.format('minecraft', dimension),
        'name': bot_name, 'delay': delay if delay != 'global' else
        config['loader'][setting_name]['delay'], 'gamemode': gamemode}
    print_plugin_message(server, info, '成功添加名为{}的bot到{}中'.format(bot_name, setting_name))
    print_message(server, info,
        '详细信息:X:{} Y:{} Z:{} Dimension:{} name:{} delay:{} gamemode:{}'.format(round(X, 2), round(Y, 2), round(Z, 2),
            '{}:{}'.format(
                'minecraft',
                dimension),
            bot_name,
            delay if delay != 'global' else
            config['loader'][
                setting_name][
                'delay'],
            gamemode))


def edit_bot(server, info, setting_name, setting_detail, setting_value, bot_name=None):
    global config
    config_dict = {
        'the_end': 'minecraft:the_end',
        'the_nether': 'minecraft:the_nether',
        'overworld': 'minecraft:overworld',
        '1': 'creative',
        '0': 'survival',
        '2': 'adventure',
        '3': 'spectator',
    }
    cfg_dict = {}
    for k, v in config_dict.items():
        cfg_dict[k] = v
        cfg_dict[v] = v
    if setting_name not in setting_list:
        print_plugin_message(server, info, '不存在名为{}的配置'.format(setting_name))
        return
    if bot_name is not None:
        if bot_name not in list(config['loader'][setting_name]['botlist'].keys()):
            print_plugin_message(server, info, '在{}中不存在名为{}的bot'.format(setting_name, bot_name))
            return
        setting_detail = setting_detail.lower()
        if setting_detail not in ['x', 'y', 'z', 'dimension', 'delay', 'gamemode', 'pos', 'name']:
            print_plugin_message(server, info,
                '不存在名为{}的设置,可用配置有: x, y, z, dimension, delay, gamemode, name'.format(setting_detail))
            return
        if setting_detail in ['dimension', 'gamemode']:
            try:
                config['loader'][setting_name]['botlist'][bot_name][setting_detail] = cfg_dict[setting_value]
            except KeyError:
                print_message(server, info, '输入值错误({})'.format(setting_value))
                return
        elif setting_detail == 'delay':
            if setting_value.upper() == 'TRUE':
                config['loader'][setting_name]['botlist'][bot_name][setting_detail] = True
            else:
                config['loader'][setting_name]['botlist'][bot_name][setting_detail] = False
        elif setting_detail == 'pos':
            config['loader'][setting_name]['botlist'][bot_name]['x'] = setting_value.split(',')[0]
            config['loader'][setting_name]['botlist'][bot_name]['y'] = setting_value.split(',')[1]
            config['loader'][setting_name]['botlist'][bot_name]['z'] = setting_value.split(',')[2]
        elif setting_detail in ['x', 'y', 'z']:
            config['loader'][setting_name]['botlist'][bot_name][setting_detail] = float(setting_value)
        elif setting_detail == 'name':
            if setting_value not in config['loader'][setting_name]['botlist'].keys():
                config['loader'][setting_name]['botlist'][bot_name][setting_detail] = str(setting_value)
                config['loader'][setting_name]['botlist'][setting_value] = config['loader'][setting_name]['botlist'][
                    bot_name]
                del config['loader'][setting_name]['botlist'][bot_name]
            else:
                print_plugin_message(server, info, '有重名bot({})'.format(setting_value))
        print_plugin_message(server, info,
            '成功将{}.{}.{}修改为{}'.format(setting_name, bot_name, setting_detail, setting_value))

    else:
        if setting_detail != 'delay':
            print_plugin_message(server, info, '输入错误({})'.format(setting_detail))
            return
        config['loader'][setting_name]['delay'] = bool(setting_value)


def del_setting(server, info, setting_name):
    global config
    if setting_name not in setting_list:
        print_plugin_message(server, info, '不存在名为{}的配置'.format(setting_name))
        return
    config['loader'].pop(setting_name)
    print_plugin_message(server, info, '删除成功')


def view_list(server, info, arg):
    if arg:
        print_message(server, info, '§7{0}§r§d配置列表§r§7{0}§r'.format('-' * 6))
        for setting_name in arg:
            pt_message(server, info,
                RTextList('§d{}§r{}'.format(setting_name, ' ' * (18 - len(setting_name))),
                    simple_RText('[§a▷§r] ', '生成{} {}'.format(setting_name,
                        '{} spawn {}'.format(prefix, setting_name)), '{} spawn {}'.format(prefix, setting_name)),
                    simple_RText('[§di§r] ', '查看{}细节 {}'.format(setting_name,
                        '{} details {}'.format(prefix, setting_name)), '{} details {}'.format(prefix, setting_name)),
                    simple_RText('[§c×§r] ', '删除{} {}'.format(setting_name,
                        '{} del {}'.format(prefix, setting_name)), '{} del {}'.format(prefix, setting_name))
                )
            )


def view_list_of_setting(server, info):
    global config
    if setting_list:
        view_list(server, info, setting_list)
    else:
        print_plugin_message(server, info, '没有配置')


def return_color(args):
    args = str(args).lower()
    color_args = {
        'minecraft:overworld': '§b主世界§r',
        'minecraft:the_end': '§5末地§r',
        'minecraft:the_nether': '§c下界§r',
        'true': '§bTrue§r',
        'false': '§cFalse§r',
        'survival': '§a生存§r',
        'creative': '§b创造§r',
        'adventure': '§c冒险§r',
        'spectator': '§6旁观§r'
    }
    try:
        return color_args[args]
    except KeyError:
        return args


def return_cmd(bot_name, setting_name, arg_name, arg, cmd_name='edit'):
    return '{} {} {} {} {} {}'.format(prefix, cmd_name, setting_name, bot_name, arg_name, arg)


def change_details(server, info, setting_name, bot_name='', arg='default'):
    if arg == 'default':
        print_message(server, info, '§7{0}§r修改§d{2}§r的§d{1}§r选项§r§7{0}§r'.format('-' * 6, setting_name, bot_name))
        pt_message(server, info,
            RTextList(
                simple_RText('[名称] ', command=return_cmd(bot_name, setting_name, 'name', ''),
                    action=RAction.suggest_command),
                simple_RText('[x] ', command=return_cmd(bot_name, setting_name, 'x', ''),
                    action=RAction.suggest_command),
                simple_RText('[y] ', command=return_cmd(bot_name, setting_name, 'y', ''),
                    action=RAction.suggest_command),
                simple_RText('[z] ', command=return_cmd(bot_name, setting_name, 'z', ''),
                    action=RAction.suggest_command),
                simple_RText('[维度] ', command='{} edit_gui {} {} dimension'.format(prefix, setting_name, bot_name)),
                simple_RText('[坐标] ', command=return_cmd(bot_name, setting_name, 'pos', ''),
                    action=RAction.suggest_command),
                simple_RText('[延时删除bot] ', command='{} edit_gui {} {} delay'.format(prefix, setting_name, bot_name)),
                simple_RText('[模式]', command='{} edit_gui {} {} gamemode'.format(prefix, setting_name, bot_name))
            )
        )
    elif arg == 'dimension':
        pt_message(server, info,
            RTextList(
                simple_RText('[§b主世界§r] ', command=return_cmd(bot_name, setting_name, 'dimension', 'overworld')),
                simple_RText('[§5末地§r] ', command=return_cmd(bot_name, setting_name, 'dimension', 'the_end')),
                simple_RText('[§c下界§r]', command=return_cmd(bot_name, setting_name, 'dimension', 'the_nether'))
            )
        )
    elif arg == 'delay':
        pt_message(server, info,
            RTextList(
                simple_RText('[§bTrue§r] ', command=return_cmd(bot_name, setting_name, 'delay', 'True')),
                simple_RText('[§cFalse§r]', command=return_cmd(bot_name, setting_name, 'delay', 'False'))
            )
        )
    elif arg == 'gamemode':
        pt_message(server, info,
            RTextList(
                simple_RText('[§a生存§r] ', command=return_cmd(bot_name, setting_name, 'gamemode', 'survival')),
                simple_RText('[§b创造§r] ', command=return_cmd(bot_name, setting_name, 'gamemode', 'creative')),
                simple_RText('[§c冒险§r] ', command=return_cmd(bot_name, setting_name, 'gamemode', 'adventure')),
                simple_RText('[§6旁观§r]', command=return_cmd(bot_name, setting_name, 'gamemode', 'spectator')),
            )
        )
    else:
        return
    return


def view_details_of_setting(server, info, setting_name, is_return_name=False, is_full=False):
    global config
    if setting_name not in setting_list:
        print_plugin_message(server, info, '不存在名为{}的配置'.format(setting_name))
        return
    if config['loader'][setting_name]['botlist'] != {}:
        if not is_return_name:
            print_message(server, info, '§7{0}§r§d配置{1} bot列表§r§7{0}§r'.format('-' * 6, setting_name))
        for detail_setting in config['loader'][setting_name]['botlist'].values():
            if is_return_name:
                return list(x['name'] for x in config['loader'][setting_name]['botlist'].values())
            elif is_full:
                pt_message(server, info,
                    RTextList(
                        '名称:§b{}§r X:§e{}§r Y:§e{}§r Z:§e{}§r 维度:{} 模式:{} 是否{}s后删除:{}'.format(
                            detail_setting['name'],
                            round(detail_setting['x'], 2),
                            round(detail_setting['y'], 2),
                            round(detail_setting['z'], 2),
                            return_color(detail_setting['dimension']),
                            return_color(detail_setting['gamemode']),
                            Delay,
                            return_color(detail_setting['delay'])
                        ),
                        simple_RText(' [§e修改§r]',
                            command='{} edit_gui {} {} default'.format(prefix, detail_setting['name'], setting_name)
                        )
                    )
                )
            elif not is_full:
                pt_message(server, info,
                    RTextList(
                        simple_RText(
                            '[§b{}§r]'.format(detail_setting['name']),
                            '{} - {} - {}\n'.format(
                                round(detail_setting['x'], 2),
                                round(detail_setting['y'], 2),
                                round(detail_setting['z'], 2)
                            ) +
                            '维度: {}\n'.format(return_color(detail_setting['dimension'])) +
                            '模式: {}\n'.format(return_color(detail_setting['gamemode'])) +
                            '是否{}s后删除: {}'.format(Delay, return_color(detail_setting['delay']))
                        )
                    )
                )
        if not is_full:
            pt_message(server, info,
                RTextList(
                    simple_RText(
                        '[展开全部]',
                        '{} details_full {}'.format(prefix, setting_name),
                        '{} details_full {}'.format(prefix, setting_name)
                    )
                )
            )
    else:
        print_plugin_message(server, info, '该配置中没有bot')


def del_bot(server, info, bot_name, setting_name):
    global config
    if setting_name not in setting_list:
        print_plugin_message(server, info, '不存在名为{}的配置'.format(setting_name))
        return
    if bot_name not in list(config['loader'][setting_name]['botlist'].keys()):
        print_plugin_message(server, info, '在{}中不存在名为{}的bot'.format(setting_name, bot_name))
        return
    config['loader'][setting_name]['botlist'].pop(bot_name)
    print_plugin_message(server, info, '删除成功')


def spawn_setting(server, info, setting_name=''):
    global config, detail
    for_kill = []
    if setting_name not in setting_list:
        if info.is_player:
            print_plugin_message(server, info, '不存在名为{}的配置'.format(setting_name))
        return
    if config['loader'][setting_name]['botlist']:
        global bot_exec_gamemode
        for name, detail in config['loader'][setting_name]['botlist'].items():
            bot_exec_gamemode[name] = {'gamemode': detail['gamemode'], 'posX': detail['x'], 'posY': detail['y'],
                'posZ': detail['z']}
        for name, detail in config['loader'][setting_name]['botlist'].items():
            server.execute(
                'execute in {} run player {} spawn at {} {} {}'.format(detail['dimension'], detail['name'],
                    detail['x'], detail['y'], detail['z']))
            if detail['delay']:
                for_kill.append(detail['name'])
        if info.is_player:
            pt_message(server, info, RTextList('生成bot成功,可执行以下操作:', simple_RText(' [§a创造§r]', '切换为创造模式{} {}'.format('',
                '{} gm {} {}'.format(
                    prefix,
                    setting_name,
                    'creative')), '{} gm {} {}'.format(prefix,
                setting_name,
                'creative')),
                simple_RText(' [§a生存§r]', '切换为生存模式{} {}'.format('',
                    '{} gm {} {}'.format(
                        prefix,
                        setting_name,
                        'survival')), '{} gm {} {}'.format(prefix, setting_name, 'survival')),
                simple_RText(' [§a冒险§r]', '切换为冒险模式{} {}'.format('',
                    '{} gm {} {}'.format(
                        prefix,
                        setting_name,
                        'adventure')), '{} gm {} {}'.format(prefix, setting_name, 'adventure')),
                simple_RText(' [§a旁观§r]', '切换为观察者模式{} {}'.format('',
                    '{} gm {} {}'.format(
                        prefix,
                        setting_name,
                        'spectator')), '{} gm {} {}'.format(prefix, setting_name, 'spectator')),
                simple_RText(' [§c×§r]', '踢出所有bot{} {}'.format('', '{} kill {}'.format(prefix,
                    setting_name)), '{} kill {}'.format(prefix, setting_name))))

        if detail:
            time.sleep(Delay)
            for i in for_kill:
                server.execute('player {} kill'.format(i))
    else:
        if info.is_player:
            print_plugin_message(server, info, '该配置中没有bot')


def kill_setting(server, info, setting_name):
    global config
    if setting_name not in setting_list:
        print_plugin_message(server, info, '不存在名为{}的配置'.format(setting_name))
        return
    if config['loader'][setting_name]['botlist'] != {}:
        for detail_setting in config['loader'][setting_name]['botlist'].values():
            server.execute('player {} kill'.format(detail_setting['name']))
    else:
        print_plugin_message(server, info, '该配置中没有bot')


def gm_setting(server, info, setting, gamemode):
    global config
    if setting not in setting_list:
        print_plugin_message(server, info, '不存在名为{}的配置'.format(setting))
        return
    if config['loader'][setting]['botlist'] != {}:
        for detail_setting in config['loader'][setting]['botlist'].values():
            server.execute('gamemode {} {}'.format(gamemode
                , detail_setting['name']))
        print_plugin_message(server, info, '执行成功')
    else:
        print_plugin_message(server, info, '该配置中没有bot')


def add_bot_al_exits_to_setting(server, info, bot_name, setting_name, delay: bool or str = True):
    global config
    if bot_name.lower().find('bot') == -1:
        print_plugin_message(server, info, '输入的玩家不是bot')
        return
    if setting_name not in setting_list:
        print_plugin_message(server, info, '不存在名为{}的配置'.format(setting_name))
        return
    if bot_name in list(config['loader'][setting_name]['botlist'].keys()):
        print_plugin_message(server, info, '在{}中已存在名为{}的bot'.format(setting_name, bot_name))
        return
    result = server.get_plugin_instance('PlayerInfoAPI').getPlayerInfo(server, bot_name)
    if result is None:
        print_plugin_message(server, info, '{} 不在线'.format(bot_name))
        return
    add_bot_to_setting(server, info, bot_name, setting_name, result['Pos'][0], result['Pos'][1], result['Pos'][2],
        result['Dimension'], result['playerGameType'], str(delay))


def add_all_bot_al_exits_to_setting(server, info, setting_name, delay: bool or str = True):
    for bot_name in bot_online_list:
        add_bot_al_exits_to_setting(server, info, bot_name, setting_name, delay)


def del_all_bot_in_setting(server, info, setting_name):
    del_list = view_details_of_setting(server, info, setting_name, is_return_name=True)
    for del_bot_name in del_list:
        del_bot(server, info, del_bot_name, setting_name)


def add_auto(server, info, setting_name):
    global config
    if setting_name not in config['loader'].keys():
        print_plugin_message(server, info, '不存在名为{}的配置'.format(setting_name))
        return
    if setting_name in config['auto_list']:
        print_plugin_message(server, info, '自启列表中已有名为{}的配置'.format(setting_name))
        return
    config['auto_list'].append(setting_name)
    print_plugin_message(server, info, '成功在自启列表中添加名为{}的配置'.format(setting_name))
    return


def del_auto(server, info, setting_name):
    global config
    if setting_name not in config['loader'].values():
        print_plugin_message(server, info, '不存在名为{}的配置'.format(setting_name))
        return
    if setting_name not in config['auto_list']:
        print_plugin_message(server, info, '自启列表中不存在名为{}的配置'.format(setting_name))
        return
    del config['auto_list'][config['auto_list'].index(setting_name)]
    print_plugin_message(server, info, '成功在自启列表中删除名为{}的配置'.format(setting_name))


def view_auto(server, info):
    global config
    if not config['auto_list']:
        print_plugin_message(server, info, '自启列表中不存在配置')
        return
    view_list(server, info, config['auto_list'])


def on_info(server, info=Called, args=''):
    contents = args if args else info.content
    command = contents.split()
    if not args.startswith(prefix) and args:
        command.insert(0, prefix)
    len_command = len(command)
    if len_command == 0:
        return
    if command[0] != prefix:
        return

    if command[0] == prefix and len_command == 1:
        for hMsg in help_message.splitlines():
            raw_help_message = ''
            raw_list = []
            raw_dict = {}
            r_list = []
            flag = False
            for i in hMsg.split('§'):
                raw_help_message += i[1:]
                if flag:
                    raw_list.extend(['§{}'.format(i[0]), i[1:]])
                else:
                    raw_list.append(i)
                flag = True
            for x in range(len(raw_list)):
                try:
                    a = raw_list.pop(0)
                    if a.startswith('§'):
                        r_list.append(a + raw_list.pop(0))
                except IndexError:
                    break
            for x in range(len(r_list)):
                raw_dict[x] = r_list[x]
            opt_dict = {}
            for k, v in raw_dict.items():
                if v in detailed_params_help_message.keys():
                    opt_dict[k] = detailed_params_help_message[v]
                else:
                    opt_dict[k] = v
            final_help_msg = RTextList(*list(opt_dict.values()))
            pt_message(server, info, final_help_msg)
        return
    global config, setting_list
    config = read()
    setting_list = list(config['loader'].keys())

    # !!bl make <setting_name>
    if len_command == 3 and command[1] == 'make':
        new_setting(server, info, command[2])


    # !!bl add <bot_name> <setting_name> <X> <Y> <Z> [dimension=overworld] [gm=creative] [delay=global(must be bool)]
    elif len_command in [7, 8, 9, 10] and command[1] == 'add':
        dimension = 'overworld'
        gamemode = 'creative'
        delay: bool or str = True
        if len_command > 7:
            if len_command >= 8:
                dimension = command[7].lower() if command[7].lower() in ['overworld', 'the_end',
                    'the_nether'] else 'overworld'
            if len_command >= 9:
                gamemode = command[8].lower() if command[8].lower() in ['creative', 'survival',
                    'adventure',
                    'spectator'] else 'creative'
            if len_command >= 10:
                try:
                    if isinstance(eval(command[9].title()), bool):
                        delay = eval(command[9].title())
                except SyntaxError:
                    ...
        add_bot_to_setting(
            server, info,
            command[2], command[3],
            command[4], command[5],
            command[6], dimension,
            gamemode, str(delay)
        )


    # !!bl edit <bot_name> <setting_name> <setting_detail> <setting_value>
    elif len_command == 6 and command[1] == 'edit':
        edit_bot(server, info, command[3], command[4], command[5], command[2])


    # !!bl edit_gui <bot_name> <setting_name> <type>
    elif len_command == 5 and command[1] == 'edit_gui':
        change_details(server, info, command[2], command[3], command[4])


    # !!bl del_bot <bot_name> <setting_name>
    elif len_command == 4 and command[1] == 'del_bot':
        del_bot(server, info, command[2], command[3])


    # !!bl modify <setting_name> <bool>
    elif len_command == 4 and command[1] == 'modify':
        delay = str2bool(command[3], True)
        edit_bot(server, info, command[2], 'delay', delay)


    # !!bl del <setting_name>
    elif len_command == 3 and command[1] == 'del':
        del_setting(server, info, command[2])


    # !!bl list
    elif len_command == 2 and command[1] == 'list':
        view_list_of_setting(server, info)


    # !!bl details <setting_name>
    elif len_command == 3 and command[1] == 'details':
        view_details_of_setting(server, info, command[2])


    # !!bl details <setting_name>
    elif len_command == 3 and command[1] == 'details_full':
        view_details_of_setting(server, info, command[2], is_full=True)


    # !!bl spawn <setting_name>
    elif len_command == 3 and command[1] == 'spawn':
        spawn_setting(server, info, command[2])


    # !!bl kill <setting_name>
    elif len_command == 3 and command[1] == 'kill':
        kill_setting(server, info, command[2])


    # !!bl gm <setting_name> <gamemode>
    elif len_command == 4 and command[1] == 'gm':
        gm_setting(server, info, command[2], command[3])


    # !!bl add_bot <setting_name> <bot_name> [delay=True]
    elif len_command in [4, 5] and command[1] == 'add_bot':
        delay = str2bool(command[4] if len_command == 5 else 'True', True)
        add_bot_al_exits_to_setting(server, info, command[2], command[3], delay)


    # !!bl add_all <setting_name> [delay=True]
    elif len_command in [3, 4] and command[1] == 'add_all':
        delay = str2bool(command[3] if len_command == 4 else 'True', True)
        add_all_bot_al_exits_to_setting(server, info, command[2], delay)


    # !!bl del_all <setting_name>
    elif len_command == 3 and command[1] == 'del_all':
        del_all_bot_in_setting(server, info, command[2])


    # !!bl add_auto <setting_name>
    elif len_command == 3 and command[1] == 'add_auto':
        add_auto(server, info, command[2])


    # !!bl del_auto <setting_name>
    elif len_command == 3 and command[1] == 'del_auto':
        del_auto(server, info, command[2])


    # !!bl auto_list
    elif len_command == 2 and command[1] == 'auto_list':
        view_auto(server, info)


    # Exception
    else:
        print_plugin_message(server, info, '输入错误，请输入§l{}§r查看帮助消息'.format(prefix))

    write_in(config)


def on_player_joined(server, player):
    global bot_exec_gamemode, player_list, bot_online_list
    if player not in player_list:
        player_list.append(player)
        if is_bot(player):
            bot_online_list.append(player)
    if player in list(bot_exec_gamemode.keys()):
        server.execute('gamemode spectator {}'.format(player))
        server.execute('gamemode {} {}'.format(bot_exec_gamemode[player]['gamemode'], player))
        server.execute(
            'tp {} {} {} {}'.format(
                player,
                bot_exec_gamemode[player]['posX'],
                bot_exec_gamemode[player]['posY'],
                bot_exec_gamemode[player]['posZ']
            )
        )
        bot_exec_gamemode.pop(player)


def on_player_left(server, player):
    global player_list, bot_online_list
    if player in player_list:
        player_list.pop(player_list.count(player))
    if player in bot_online_list:
        server.say('§7bot: {}已下线'.format(player))
        bot_online_list.pop(bot_online_list.index(player))


def on_server_startup(server):
    global config, setting_list, player_list
    config = read()
    setting_list = list(config['loader'].keys())
    player_list = []
    for setting_name in config['auto_list']:
        spawn_setting(server, Cls, setting_name=setting_name)
