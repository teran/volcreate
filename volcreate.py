#!/usr/bin/env python

from optparse import OptionParser
import os
import re
import subprocess
import sys

from flask import Flask, json, render_template_string, request
import lvm2py

app = Flask(__name__)

parser = OptionParser()
parser.add_option('-g', '--group', dest='vg_name', help='VG name to use')
parser.add_option('--host', dest='host', help='IP address to listen', default='127.0.0.1')
parser.add_option('-p', '--port', type='int', dest='port', help='Port to listen', default=5000)
parser.add_option('-i', '--iscsi-storage', dest='iscsi_storage', help="SAN network IQN part of iSCSI storage name")
parser.add_option('--tgt-confdir', dest='tgt_confdir', help="tgt daemon config file directory", default="/etc/tgt/conf.d")

(options, args) = parser.parse_args()

if options.vg_name is None:
    parser.print_help()
    sys.exit(1)

lvm = lvm2py.LVM()
vg = lvm.get_vg(options.vg_name, 'w')

def sanitize_lv_name(namespace, name):
    namespace = re.sub("[^a-zA-Z0-9]","", namespace)
    name = re.sub("[^a-zA-Z0-9]","", name)

    return namespace+'-'+name

@app.route("/tgt/<string:namespace>/<string:name>", methods=["POST"])
def create_tgt(namespace, name):
    try:
        body = request.get_json()
    except:
        return json.dumps({
            'status': 'error',
            'reason': 'Error parsing incoming JSON'
        }), 400

    volume_name = sanitize_lv_name(namespace, name)

    template_options = {
        'volume_name': volume_name,
        'vg_name': options.vg_name,
        'iscsi_storage': options.iscsi_storage,
        'initiator': body.get('initiator', '127.0.0.1')
    }

    try:
        fp = open(os.path.join(options.tgt_confdir, volume_name+'.conf'), 'w')
        fp.write(
            render_template_string(open('/srv/tgt.conf.j2').read(), **template_options))
        fp.close()

        subprocess.call(["service", "tgt", "reload"])
    except Exception as e:
        return json.dumps({
            'status': 'error',
            'reason': str(e)
        }), 500

    return json.dumps({
        'status': 'ok',
    }), 201


@app.route("/volume/<string:namespace>/<string:name>", methods=["POST"])
def create_lv(namespace, name):
    try:
        body = request.get_json()
    except:
        return json.dumps({
            'status': 'error',
            'reason': 'Error parsing incoming JSON'
        }), 400

    if body is not None:
        size = body.get('size', None)
        units = body.get('units', None)

        if size is None or units is None:
            return json.dumps({
                'status': 'error',
                'reason': 'Size and units must be specified',
            }), 400

        volume_name = sanitize_lv_name(namespace, name)
        try:
            vg.create_lv(volume_name, size, units)
        except Exception as e:
            return json.dumps({
                'status': 'error',
                'reason': str(e)
            }), 500

        return json.dumps({
            'status': 'ok',
        }), 201
    else:
        return json.dumps({
            'status': 'error',
            'reason': 'JSON body must present with volume parameters',
        }), 400

@app.route("/", methods=["GET"])
def list_lvs():
    try:
        lvs = vg.lvscan()
    except Exception as e:
        return json.dumps({
            'status': 'error',
            'reason': str(e)
        }), 500

    return json.dumps({
        'status': 'ok',
        'volumes': [x.name for x in lvs],
    }), 200

@app.route("/tgt/<string:namespace>/<string:name>", methods=["DELETE"])
def remove_tgt(namespace, name):
    volume_name = sanitize_lv_name(namespace, name)
    config_path = os.path.join(options.tgt_confdir, volume_name+'.conf')

    if not os.path.exists(config_path):
        return json.dumps({
            'status': 'error',
            'reason': 'tgt object doesn\'t exists'
        }), 404

    try:
        os.unlink(config_path)
        subprocess.call(["service", "tgt", "reload"])
    except Exception as e:
        return json.dumps({
            'status': 'error',
            'reason': str(e)
        }), 500

    return json.dumps({
        'status': 'ok'
    }), 200

@app.route("/volume/<string:namespace>/<string:name>", methods=["DELETE"])
def remove_lv(namespace, name):
    volume_name = sanitize_lv_name(namespace, name)
    try:
        lv = vg.get_lv(volume_name)
        vg.remove_lv(lv)
    except lvm2py.lv.HandleError as e:
        return json.dumps({
            'status': 'error',
            'reason': 'LV object doesn\'t exists'
        }), 404
    except Exception as e:
        return json.dumps({
            'status': 'error',
            'reason': str(e)
        }), 500

    return json.dumps({
        'status': 'ok',
    }), 200

if __name__ == "__main__":
    app.run(host=options.host, port=options.port)
