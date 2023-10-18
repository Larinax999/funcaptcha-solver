from httpx import Client
from base64 import b64encode, b64decode
from random import randint,choice
from json import dumps,loads
# from subprocess import check_output
# from secrets import token_hex
# from PIL import Image
# from io import BytesIO
from datetime import datetime
from time import sleep,time
from Crypto.Cipher import AES # pip install pycryptodome
from util import SSL
import tzlocal, math, hashlib

_KEY="sub_1MvmpeCRwBwvt6ptM658pgpB"
_UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.48"
# resolution=["1920,1080","2560,1080","2560,1440","3840,2160","3440,1440","5120,1440"]
# graphics_card=["GTX 1050","GTX 1060","GTX 1080","GTX 1650","GTX 1660","RTX 2060","RTX 2070","RTX 2080","RTX 3060","RTX 3070","RTX 3080","RTX 3090","RTX 4080","RTX 4090"]
Cliimg=Client(headers={"user-agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15"})
Clicap=Client(headers={"user-agent":"FunCaptchaSolverBylarina/0.1"},timeout=15)

def pos(id,method):
    x=(id % 3)*100+(id%3)*3+3+10+randint(1,80)
    y=math.floor(id/3)*100+math.floor(id / 3)*3+3+10+randint(1,80)
    if method=="method_1":
        return {"x":x,"y":y}
    elif method=="method_2":
        return {"x":x,"y":(y+x*x)}
    elif method=="method_3":
        return {"a":x,"b":y}
    elif method=="method_4":
        return [x,y]
    elif method=="method_5":
        return [math.sqrt(x),math.sqrt(y)]
    else: # default
        return {"px":round(x/300, 2),"py":round(y/200,2),"x":x,"y":y}

def encrypt(data, key):
    # Padding
    data = data + chr(16-len(data)%16)*(16-len(data)%16)
    salt = b"".join(choice("abcdefghijklmnopqrstuvwxyz").encode() for x in range(8))
    salted, dx = b"", b""
    while len(salted) < 48:
        dx = hashlib.md5(dx+key.encode()+salt).digest()
        salted += dx
    key = salted[:32]
    iv = salted[32:32+16]
    aes = AES.new(key, AES.MODE_CBC, iv)
    return dumps({"ct": b64encode(aes.encrypt(data.encode())).decode("utf-8"),"iv":iv.hex(),"s":salt.hex()},separators=(',', ':'))

def decrypt(data, key):
    data = loads(data)
    dk = key.encode()+bytes.fromhex(data["s"])
    md5 = [hashlib.md5(dk).digest()]
    result = md5[0]
    for i in range(1, 3+1):
        md5.insert(i, hashlib.md5((md5[i-1]+dk)).digest())
        result += md5[i]
    aes = AES.new(result[:32], AES.MODE_CBC, bytes.fromhex(data["iv"]))
    return aes.decrypt(b64decode(data["ct"]))

# def Getbda():
#     false=False
#     null=None
#     true=True
#     ms=time()
#     # feh=check_output(f"node murmur.js \"{', '.join(fe)}\"").decode()
#     n=b64encode(str(int(time())).encode()).decode()
#     return b64encode(encrypt(dumps([{"key":"api_type","value":"js"},{"key":"p","value":1},{"key":"f","value":"53080946d3ccdfb69b9c6239e38398ac"},{"key":"n","value":n},{"key":"wh","value":"c91ad2eafa9d036bb0d8208afeaa318d|72627afbfd19a741c7da1732218301ac"},{"key":"enhanced_fp","value":[{"key":"webgl_extensions","value":"ANGLE_instanced_arrays;EXT_blend_minmax;EXT_color_buffer_half_float;EXT_disjoint_timer_query;EXT_float_blend;EXT_frag_depth;EXT_shader_texture_lod;EXT_texture_compression_bptc;EXT_texture_compression_rgtc;EXT_texture_filter_anisotropic;EXT_sRGB;KHR_parallel_shader_compile;OES_element_index_uint;OES_fbo_render_mipmap;OES_standard_derivatives;OES_texture_float;OES_texture_float_linear;OES_texture_half_float;OES_texture_half_float_linear;OES_vertex_array_object;WEBGL_color_buffer_float;WEBGL_compressed_texture_s3tc;WEBGL_compressed_texture_s3tc_srgb;WEBGL_debug_renderer_info;WEBGL_debug_shaders;WEBGL_depth_texture;WEBGL_draw_buffers;WEBGL_lose_context;WEBGL_multi_draw"},{"key":"webgl_extensions_hash","value":"58a5a04a5bef1a78fa88d5c5098bd237"},{"key":"webgl_renderer","value":"WebKit WebGL"},{"key":"webgl_vendor","value":"WebKit"},{"key":"webgl_version","value":"WebGL 1.0 (OpenGL ES 2.0 Chromium)"},{"key":"webgl_shading_language_version","value":"WebGL GLSL ES 1.0 (OpenGL ES GLSL ES 1.0 Chromium)"},{"key":"webgl_aliased_line_width_range","value":"[1, 1]"},{"key":"webgl_aliased_point_size_range","value":"[1, 1024]"},{"key":"webgl_antialiasing","value":"yes"},{"key":"webgl_bits","value":"8,8,24,8,8,0"},{"key":"webgl_max_params","value":"16,32,16384,1024,16384,16,16384,30,16,16,4095"},{"key":"webgl_max_viewport_dims","value":"[32767, 32767]"},{"key":"webgl_unmasked_vendor","value":"Google Inc. (NVIDIA)"},{"key":"webgl_unmasked_renderer","value":"ANGLE (NVIDIA, NVIDIA GeForce RTX 4090 Direct3D11 vs_5_0 ps_5_0, D3D11)"},{"key":"webgl_vsf_params","value":"23,127,127,23,127,127,23,127,127"},{"key":"webgl_vsi_params","value":"0,31,30,0,31,30,0,31,30"},{"key":"webgl_fsf_params","value":"23,127,127,23,127,127,23,127,127"},{"key":"webgl_fsi_params","value":"0,31,30,0,31,30,0,31,30"},{"key":"webgl_hash_webgl","value":"ff2121bc6f4faae22bb7a13a31f9e92d"},{"key":"user_agent_data_brands","value":"Not_A Brand,Microsoft Edge,Chromium"},{"key":"user_agent_data_mobile","value":false},{"key":"navigator_connection_downlink","value":10.0},{"key":"navigator_connection_downlink_max","value":null},{"key":"network_info_rtt","value":50},{"key":"network_info_save_data","value":false},{"key":"network_info_rtt_type","value":null},{"key":"screen_pixel_depth","value":24},{"key":"navigator_device_memory","value":8},{"key":"navigator_languages","value":"en-US"},{"key":"window_inner_width","value":1996},{"key":"window_inner_height","value":700},{"key":"window_outer_width","value":2060},{"key":"window_outer_height","value":819},{"key":"browser_detection_firefox","value":false},{"key":"browser_detection_brave","value":false},{"key":"audio_codecs","value":"{\"ogg\":\"probably\",\"mp3\":\"probably\",\"wav\":\"probably\",\"m4a\":\"maybe\",\"aac\":\"probably\"}"},{"key":"video_codecs","value":"{\"ogg\":\"probably\",\"h264\":\"probably\",\"webm\":\"probably\",\"mpeg4v\":\"\",\"mpeg4a\":\"\",\"theora\":\"\"}"},{"key":"media_query_dark_mode","value":true},{"key":"headless_browser_phantom","value":false},{"key":"headless_browser_selenium","value":false},{"key":"headless_browser_nightmare_js","value":false},{"key":"document__referrer","value":null},{"key":"window__ancestor_origins","value":[]},{"key":"window__tree_index","value":[]},{"key":"window__tree_structure","value":"[]"},{"key":"window__location_href","value":"https://www.roblox.com/"},{"key":"client_config__sitedata_location_href","value":"https://www.roblox.com/"},{"key":"client_config__surl","value":null},{"key":"client_config__language","value":"en"},{"key":"navigator_battery_charging","value":true},{"key":"audio_fingerprint","value":"124.04347527516074"}]},{"key":"fe","value":["DNT:unknown","L:en-US","D:24","PR:1","S:3440,1440","AS:3440,1400","TO:-420","SS:true","LS:true","IDB:true","B:false","ODB:true","CPUC:unknown","PK:Win32","CFP:-1933402981","FR:false","FOS:false","FB:false","JSF:Arial,Arial Black,Arial Narrow,Calibri,Cambria,Cambria Math,Comic Sans MS,Consolas,Courier,Courier New,Georgia,Helvetica,Impact,Lucida Console,Lucida Sans Unicode,Microsoft Sans Serif,MS Gothic,MS PGothic,MS Sans Serif,MS Serif,Palatino Linotype,Segoe Print,Segoe Script,Segoe UI,Segoe UI Light,Segoe UI Semibold,Segoe UI Symbol,Tahoma,Times,Times New Roman,Trebuchet MS,Verdana,Wingdings","P:Chrome PDF Viewer,Chromium PDF Viewer,Microsoft Edge PDF Viewer,PDF Viewer,WebKit built-in PDF","T:0,false,false","H:32","SWF:false"]},{"key":"ife_hash","value":"c5ff6eafde7cc7876906817e32217fb1"},{"key":"cs","value":1},{"key":"jsbd","value":"{\"HL\":2,\"NCE\":true,\"DT\":\"Roblox\",\"NWD\":\"false\",\"DA\":null,\"DR\":null,\"DMT\":27,\"DO\":null,\"DOT\":28}"}],separators=(",", ":")),_UA+str(round(ms-(ms % 21600)))[:-2]).encode()).decode()

# a="eyJjdCI6Ims4MURoOHpzaGpoc3VSNGswZzBSRFlBejA4NUtGNkpQeFpTak5vK1A2cElTUm1KL2NpWGZUU2hSelNVY0p1SmRDa1RWMjJHcmt6djllSWNaUzgvU0ZCNFZLR2kvOERCNnIrck5sUVJVcVlTM0xHRnFwcElQOStZSm56ZHVubmdEbEphN1gzcWg2MEJVSVlmVE85emRERGhrbnRDbnY2KzhZZ1ZDWnIwc09URzZJczdXQUJpVXZQZG5pTVNXRGlTLzVWaENJVXhwejUwRUtpUHNvenlXSlQwMktJcHpnc1JlQS81TmdlM0JCQW5wc1pMalRnUjJIelJxZWxBdGtMeDJsUFBPYWF2bUZWTi8vMFZhcU54d3Jxck1MRkQ1eVcxODBwQUdhTWNaekhNT0c1ckVOT3pnVHA5SGx2dFlueWFldWdNbkkzbmZtcjhSMTNENmU4ckd0VWZxeEZ0M1Bja1RMd3Z1Z0VGbnJ5bWI5T3BYc3FUSWcySVlOallzQmJGWTdkeElya1lSb0psK1VGOVR5TllmaDBIbGNOeFFMWDJmWnZrRTBrVk55ZWdSUkdXOUxjeWNBcnV3TzYxV0FVemRobHBXaUJEcWQzbkNwb29Hai9rQ3NvMi92UlRoU015bGVxaWtsVWtkM0duMnM5NkljODdpSlJnVlJlWXNsZEJNZVd1emNyUUZpWVNlUW1KOXgwWkJzSHhSSlA4NTNjZC9ZUHhuMFVSN3FZTkRPVlFDQlljTm5Xc2dvdXRPdlRNNnVMRVdlUnJYeEh6aU1FSi81NW9YUUJmZTl5MytjWktRamZVdWVQYXBybEloZ25VZ1o5ejFsSmJoS2xIMmExbmhobDFNQytGYVNDc09uYTBiM2dwTXhSSTVJZEFlaFlidS9UVzFwNjBaeHRndlFGcWhzWDNCV2xlYjZ2ZGc5dkhjZjV6cmdTa1B1cHJncHNLVWY0Q09xNXdqU2RVdlZJdWpUSitvYVVCWGtlTXU2WXBWVkhRSldSay9nR2RuNkIzNzVvc29zd2IvVWxlcnd0ZW1ETFFpMGFIR0RCUVgvelU0VkJPTjQzcVZHQnY2RjBYOWFVMDF0TTR4TVUzUlFlbHUzRzJWMjhDSHI4RjhXM25xY1lCTTNYSVpGZ0FSZFU0cktnT2JDai96UG9MbStYN093S1MyVEgzN0xRUTU5cjR0WnpLK0I5QTJXUVlHdE5CaHlPd3QxRHFkNWNBcXowYkUyNkZwVW1odjhnT2owaWpNQTZJbHlXb2ZldTU5eHdzT0p3MDVCbkJCU3NvRmxtQldPN014dUxBQjJENlNxUXZlWm81bStiSTBEVVlIN1JPSi94MWxOT3dPOHErSGExaG9zbWF4c1l1UnJZeVV5SDlXVEtqeFVGMzNIMklINGhPSW1NaGdnSzQzUXhQMURWSHo4RTVyWkFEVWEzS0gvOE9Wa3JFekN2aTQwNmJhQlpGblZyTnZ2K1loRlN6OUp5VHJFUkVtV1NyVEpuUmpqdmJ4SHdsNHNlQlB6d25XZTg1V083cmxkNzFjZDZXRWxXSktCdHpwcDVrMCtiVkRJSXE5eGJCVEc2S3IyRVQxbGkvYlZzOW9yTXRQc29ZaE92d2pmeWgySFlEV0FMY29vVUU5KzVSVWkwYVBYSEpUdDJFNlNGNkd1a0o3WmRGZHg4Uk04MS9zRnpkdHhXTXFPclRmTXJZMjd2dzZxR05BblNEQ3o2VTd2aEZURW4yNzFGNUt0L2FFSnZCbXBNelFZRk5NUGVqc256U3dsM0Z3NldoSHRBanBBU1I2SDhVMGdjN3Y3NWlFUG5KUlBWc05vbmdZUGpLNytwUmR1cDBzVWNuMzFocHpwcXdWL3NzaC9hdDN4UjRScUVGWjdGNXBwWUhFeldEdjNBUFhOQXhJTy9kMGNRVGxRQm5TeFR0eGIrbk9TRkovYVNPUlhQZ2FYeXVPMXlENU82ZEVFeVIxZ2xqRngzQ1RyalMvOW14c3d1RGRzM1pUZ1ltY2xHZjM0d0ZpOHYvWDc3b2JTLzJkekZDZEtuN3BZVEI0RmJob094cmdUYVFxaXlWR0ZMYVp2UWJ3N3VIR0hMc0VFdUE5MnZWRkh3UWRiSGQ3ZlY4NHNBU3JrL3djeVJNNVVNYUVCK0RXU3RlakpxYmpaUEQ3VDBTZ1lSZHdnNXdLNWN2U1RENkpSTkRBTzkrYjBldFB6eDhmZFR1cExnWVdUbDNsZ1h6QmN4WHZpaE1pRlFmYWhyWVpGZUp1aHI1VjFUeFRRODVGVmJZajhOMFZ4OUhwL0FtaHpNSTA2NUNEVmp5MHVzalNSbHV0ZDVRTEV6TDk2UTlIb2hZckVWNzZrcklMVEpoRDFpUUtEeWlBcFhzU0dLbUV5VmRCNVRHazB5VmRnRVRpcE14eUowTnNtNHZmYit6Wlp4TTdHQzMvNTEycmYzS2Q5YnNYd256QWhZaUc0VlZYc3VXb0JQTUNVOEI1d0JvTDRZQlpMeThnNTIxVjhCS3pVWUp2aEJ6S0hzc3M1M21WSzl5Z3JKSDhiZUVUMmtkc2dKNGlzRkpuMXc4T2dmZjA4Uy9yRHVsSVZLcEIxeTJISDZwSFZSVXpiaUdyenRGTzJoQkpBY25XcmNZVFAxYzJOeFkwdCt2cHlwRVFpVHk3RjN6VG9kYWZqbXhxMnVtcmZlSFU5eEwwUmpVK0dTL1hwbnRjd3drRE5DODNxOHRpNDZhWWt5OFplRVVyaUdKZ0VMWldZMXg0TDlRa0ZjSVhIbVc4Z0wwSEF1ZG51b1poRFVpVkE2dWdYblpBYWdxM3BUNnQ1SmYzdlVuOThRZGFDcGtjcEZQUWJWNkExcWo1MjNEenZhOXNVdytzaHlTUXNod1RiUVF2QnFxTXY4YnhRMVYyMzRnTTAwR25RbnNickNuVW9vR0RoN0RFb2ZsTTNIcHYybFcwcXUxaThFQlRPY0ljNC9Od2I1WFROTFRJMEhaMzUxZE1xV1RFYWpkbzMyNEE0Wnhmb0pSOU8yWVZDWHNLUFJpb2ZCclY3WndBVG81KzdDVHFqTGlpL0JLT3o4VjJ5S1prOVJwTWJFSEMxZ1MwRUJIbEo1bDBtMk01djZqdml4UFRtUWlOWXkzVHBOSm1leXRFQW5USzRqWi9oa0k1b29zUTVBUEVHV1IyeDZGUlB6SkdaTERiRTNlN3FNU2tTMXlBTkVoWDBjazRmeDFsMVJHWWxZTTJJMUZsUXFheUxUYjdOYjFyU21oMVh1cXVUTUU2OVhZOHp1ZWc4aWtLT3JsTlVyVmsweUM4aWhqNU1ESnBIZWtHRWsrUVg5N3ZmcFM2N0NEOStYZGp2bVU4eTIrWkVtNmpoa01MVHVCQ3d4UDNRRFg0SUx3REtYd05Wc2ViY2QwYnFUeU5hUXBJWVNPOXNQS295dDVOV2MwdUVzT2JGalFOanA2NHBVaFNXWjR0bHFGSGFLOStGZnNBQ2xnK28yeS9BeFB0R1NMd3NvOFh6VWRXNVVPSlVOcVJWMlhZcFJqNkNWRC94T3N2dWNsZ2tNNmpaVWhsckE1LzJzTHZwNU4zdndsYmFlNVhJRXFJZWFzb3RvTVJtU3JmS3BKdERVWDRudFRES3B2ZkNmRDV6eFR6M2xNWFdXZlZ1Y2tRMmVjeUIwdEJPdXFlYndRVlJLRmNQTklicDJQKysxRmEybzRlWUZQRWRjZ1N4OTd1OFZPdUcrbnYweXByUHV5YVhvTGVaa0xkODlWVEQrTWRWZlRSTURQUmF0djVYQmNsSFM0RDJYa21Gc2tYemYyWGxncm16OUVkUk01MVpqZFV2NC9tL2hIenpVU0plb2FTQ3BpblpWcmprRXRSbERsYitDR0dERjZTdzl4MjVZcjVNQmNmOE1ySUdydUh5MWNnVmJUTjk5NUZreEMwcnRlLzZoaTNKTXhHUkFkZ3VRaHV4YUlUc2RvcVFPbUo4aXVMQ1lmZkpGZXNPd0VoYmZkK1JSSjFjWDVYOHFyL1pYMkJVVjhzY0tLdUtkcmpaSGs1cUdPd3pML0RyM0IxOHBEbzJDbU9YM1RzQnJvcGZ3SHZhd2xJZW9VcndVREhmU0NweENLVWRqZklnQThXellnRDdpazVxNWVRYWd1S0h1aDdObUd3ZzFYdE1Fa1hTNHBNTTlFaWJRbjZxVkZ6REtPandJWUZ1Wm1jb0R2NWRSeDkwYVJTQ2FEYTVCSndhSDJmZFpIa3RwNkNORGV0cG85RVNYazZ2SjdHM0ttbkdKWHBqbTc2NTkxSjNTenNxQWQrVEQyR1lYVXRBWUl5YjR1OFRYUDN3NnVsTWRzekdkeVpDbW41c3hzZTVYU2ZrWUxLWFRScHptYUo1ZHcvdHBSRnoyQXEyL3cvTTMvb2t3bDJkcUcvM05aZWx2ajFuSjM5cEVETmdHeXBRZmpnOTlSc1dQS1R1dTJ3czlsUm5FK3NyVWthMURPRW5qajhGcDhDbEJ5VTdDLytWOStiYnFqN0VjRDhuWUpsRW9iYnR3TG9jaURxSFdTMnpwL1dYdW9EVGFMYmFrM1FTT2Q2MjB5TUN6ZDJ1WFFPQzFSNXVaTlJDZllvWmZQMEFLeDRmbnZBZlNISTQrcW5PKzJzL2JlU1UzSElValR6aHNMRCtDcmUvU1Jrd2N5OTVBSm8vWVZ0TFovSXZoRDNXdUhHUjh2UTBtM3ZRSmptcmRxOE9Hc00rVWY4SVJKZGdVWVBPak93cWNXQnZKVjNmWms0d0dXM0lqLzRSV2FwQzFFY0wvRk9EdzVHbmlpVnFZNTZwU0lrK0JKbVRTSE9XSDVyUGJsQ1hMbDJMTGpoSi9jY1NYSnFCZ3VhRFdjL09NTHp1QkFwWEhsRzZjenp1ajR1RkNqbXZkUStkRHNISGVPR25qTFpyRzFzNVA4c3lwTXp5eXFkbU14NkR6eHMrd0w2eUFuU0FaM2JJLzhhMUpTSEJuRGVsSTBrVVdNUm1zVkxNeE9UaE5yZkR3UzB2S0FIdmNUZGdwV3dyTjYwL01KRllYa2tKNFg0N1dOdlZTd25SWWhyNWY2V0JnWlA0QWYxZHlmRG9sWnhCbG1iRElBM2dBL2tQTm5aVVBDZlZ3UTlqUnJ1bHJvQU9wanBwa1BYNmVZeldjTlRpdVV5SnRQY0F6VVl2Slo2WkpFZ01QdGhtZVl5bzZFR3F2RXFGVTFwWllMQk5sMkV1elVuTnc3TmVxZ0VKQmdOTkNCKzFWNlE1ekJnUzBTY085ZlJ5dS9qSTBxeEdjSTE3RnBPbU1LMWZVVnRkNHUwWkR5QTdsT0pLVnRmcU4zbDJVSFJWOW9SSnJHV3UwOUh3Z0tIK0VtQjR6TXZyaEZldE8zZnFhQmlSU05BYlR2TWVHL1k2MlZpSFFQeGZHZFJQVHJ6WFB0QzR5MUxNSDVIMkNPWWpDdldvd0paWjBnUkhSMWVXbWRocVVLYmtyWDA0cnVMZGU3cmRIalV5TnVRSFcxZUF4YzhaZElPaHZTYTRMdlF3L0I0TllHNVZvL0RVSzgwOVFCVXFwU1ZJVUJHWlUrYUwxdzczdFA2MFl2MHFCbkhVK3l1TDhTNlBUdWdveXJ1dm1DaXNXR21MNGRnazRXV0haNzJ0SXJnTk9Sc3M4c1YzT3ZSMDAwbjZhZlhoRkx5MkFnWHlUelBQL1NMWHV0V2dDSEdLUG5oSUZha0lyeEFjN2F0cDhsRDA2dXRZdm9yQXVCZDd2VFYycUVrcmo0VEUveERtOGR1cG9SWi90K3d5cDBtUWl5ak1ady9wcXZ3dUdoNCtub3pkekQxcW1GRk1MZ0c1VnhSamtUWXhUbTFPTDBPOXkwNVhYQzJJS3dKbzV6aStBYU1KWDRDKzNkY29SNzBOL05jZU5BQ2t5T2FJSUthWkNvRU9CV1BiSkdESWZUYnpEWDRLWVBkZ3RUTSs0UkhSN293R2pYcGgvYjdpQ2lTWS9aekN1UmJiVTAzVFZUd09MV05aRG51ekkydHZrNzZ4RTEvVEZLWkpNbExPOWNFTjd2bEJzT0hZZUR5cHp5RWYvMkFoNWY2YkdKbFVyQ0NDQk1GcEZLWEdsT0h1Q2h1dmJRckFPekt3aGc3aHBHY0dNS3VDZTNaaWxHcHVQd1dDdWpQTHRlNmc3T3RrdGd1Y0dpWmZvZVpGZWEvNlFCZ25SWk1GSkRpVmNvZDl1SjlTVGRtd2Nrb2Y3N3VRajBrVHpxVFZsZFpNeFlQZkhvL1VvOXlkaUVCazM1cGZMV0xYRlZ2TEV3MkZmOUY3emV6T1BBSTJSdVJkSDR5MnJybW1Vc2Vqa2UyNURtOTdIZ3NQMW1Uc0hXdVpMWEx3S0JxOUpRYUlzVU1hZDlXM0VyVjh6SHY1YU5oZW9XZUdJdjh1ZEZxU3lzSis0cGFXMyt6RmgvOVVQZXVmd3BCeU5WdmhKTVZ3UFBKOFFPdDNQTnJ3Z0E5WUNYNnB3WURVZmJRL0xCaUZheEJkSjF3Tnc4bFp5ZjVuSXBUMVljb3E5Yi93S0dKSDZKMXdUY09TRVdGN0thYUNtM3pEc2UvcGVmL01PbUdJUmk1dXJxSmhqTHZmaXNNVldmWnJtOFhHVVY2L25xWnR0NzJ5UUhwdFRydU5LTWpkdE1QK0FGc296MWFaeFhRdHNoR0dRMzhPZTFtTHdwLzNmYmJVVHBZWHZxaWxhaXlsVGtZRU91aUtEZXVua3E3aERBL082KzAzZFB4cDhHLzZhWTlJTjF2STF3bEFGRVhTbHFNY0g5bnJoR2cxV1lhTEFRYXhzallpcndzS1pLdDlNN2xkS2YzY0RPdXZXQzBHU1hGMDRCQkUrS3dwWlJkbWRhN1NBdjBqd3VzaWFWQVVwSllNVGphYUxGaDFCRFcvTkVsRjRNcHdHekM3Y3pkc0dVNWROYzVIQnErMXhGM094bWJ5QzNBcFBTdCtNMWhiSDJOZlAvREc4NTVXY3phV2hqRFJiM0VOaGxmLzd3ZjRKMFhuTXU5cy8rYzFiR3EvTHU3TjN5akx2cFJ3T1ZUTDhKYUtZems2NkVsNGw1aDlDanM2RThLYXlpRE12UnBkUGhXVzhTS01HLzd1MnBpWHVFT0lRTzRhVHpKdUY5eEVGTHhmbWxXZWN1WmlMNmY3N3l3emNYMWhuZGFVck8wTlVEaTYzYUY5dSt1RVZrUXNBMnNBc0VySjVDRDJwVnlQRjcyYytucEhncW95UVB6WGhia2dQT2JTb2pVT0NIelJrSmxMK216QlYxQkZ2cThSQllVdUVzMytVRm9td3ZWVDZoa1I0eUU5b2NLbVVZYmNJdng4alY4QThUdU9HMU5rS3RLNGFueHlwOFB4VDhhUUhSS28weUNPaWlZbWY4c0orUXA5M1RFNmR4dDBadTJaWWx4TTBVTzVMV0VLSW5aczN2SVpkRkF0ZEgyREJRYjI2aUtzNk9QMDhVSS9pdnphcWs4OXAxalBNb0VsTVJ1ZjNTdm53MmhhVHZlQmR2Y1hJOHI0MTRtUjBkRzBjdXV3Y1F3dW9VQnE2dWlnL2NUYTRTQzg5NC9zZndPRjc1RjlFLzhCKzZORzRBNWpOcEhlZkkxQjFJYWlERzl6MDViV1ZBS0ZjSEh5VXVJelRjUDdRdkxKRFJGeXhoVGpHYk5WdDZSZzBrT3p3QzdmM1pyU045Mzk5dnhMc2JaK21PU21nZy9lNXI2ajY0ZWVaQ2ZKaTR0cUJhcHl4UmJXMEdEM0pROVRiSDRpRGVYczU5b1FJOTFkazN2N2t4NExSbjBmdUFOY1FmcW90RUM2K1hrQmZmTUZoaWovNm1tTm9SREhYTXgwZUNmcmxXWUJmTlQrR0J0QmhzV3VWeGxyQ2Q2WU1MS2h1LzNwZUJYSEQ5QWY3YklIeXpxMlVSR2Z4STRzQWtTY2V4VWZmcWptZENhbmNpYWZENjV0Q0M5ZTk5QjJXd3NGRm1vRzI1c1JyaERNeW05STd2TUt5WjRtdStjMThqZ3pQMmNtYTFVaitCazQyRjhLck9SNDRrakZIUnp1eExETk9HaFN6d2RnT3pVN3lPak9VY1FodzVlVE15SUlqbXpLUWpQcGZNakUrcjlPZzU3eFJoeVZIa3JDZFVoaUtJUDdzUEhKajRqcTB6bjdNVldKM2xlY1JIYTNaUFVVVzlYbElFYnBrM2RBcVFjQTNhNVh4ZXVrUjQyeWRMcENHdnNyR2hIVitkWS8wWEZXRHB5bVNqL2FYOEkzWTRHMlJwUmp4eVlRR0RmQ0pWalFSeGRORFJ0Z1FDdlRrVkl5OUF2aGt0VTYwbW0xOTNGK1I0T3JnYlZINlRIOWpWTHpYUTdzSUUzaGsyYWdJb2dnN2lSMlJPSDFYK2lZVmYvaHlQK0VPc0VjZXdIWEZmNHFwa3dNeGpESEF6Wm9vQ3RpbVllaGVweCIsIml2IjoiYmNjZGQ1NGQ1OGY1OTZiNGNlNzQxODJhNmI0YjNmNDYiLCJzIjoiMmViM2M4NzRjNmU5ODljYyJ9"
# u="Mozilla/5.0 (iPhone; CPU iPhone OS 16_1_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Mobile/15E148 Safari/604.1"
# ms=time()
# print(decrypt(b64decode(a).decode(),u+str(round(ms-(ms % 21600)))).decode()[:-14])

# ms=time()
# print(decrypt('{"ct":"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","iv":"41199bb0fdcb5f524530286be2ac58fe","s":"91b7e6243f548f7c"}',"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.64"+str(round(ms-(ms % 21600)))).decode())

def Getbda():
   false=False # shit code lol ;>
   null=None
   true=True
   ms=time()
   n=b64encode(str(int(time())).encode()).decode()
   return b64encode(encrypt(dumps([{"key":"api_type","value":"js"},{"key":"p","value":1},{"key":"f","value":"cd368cac27e1443f07838c8014f0c9e1"},{"key":"n","value":n},{"key":"wh","value":"2968a26a6998e7b72c81b7b2e35b974f|72627afbfd19a741c7da1732218301ac"},{"key":"enhanced_fp","value":[{"key":"webgl_extensions","value":"ANGLE_instanced_arrays;EXT_blend_minmax;EXT_color_buffer_half_float;EXT_disjoint_timer_query;EXT_float_blend;EXT_frag_depth;EXT_shader_texture_lod;EXT_texture_compression_bptc;EXT_texture_compression_rgtc;EXT_texture_filter_anisotropic;EXT_sRGB;KHR_parallel_shader_compile;OES_element_index_uint;OES_fbo_render_mipmap;OES_standard_derivatives;OES_texture_float;OES_texture_float_linear;OES_texture_half_float;OES_texture_half_float_linear;OES_vertex_array_object;WEBGL_color_buffer_float;WEBGL_compressed_texture_s3tc;WEBGL_compressed_texture_s3tc_srgb;WEBGL_debug_renderer_info;WEBGL_debug_shaders;WEBGL_depth_texture;WEBGL_draw_buffers;WEBGL_lose_context;WEBGL_multi_draw"},{"key":"webgl_extensions_hash","value":"58a5a04a5bef1a78fa88d5c5098bd237"},{"key":"webgl_renderer","value":"WebKit WebGL"},{"key":"webgl_vendor","value":"WebKit"},{"key":"webgl_version","value":"WebGL 1.0 (OpenGL ES 2.0 Chromium)"},{"key":"webgl_shading_language_version","value":"WebGL GLSL ES 1.0 (OpenGL ES GLSL ES 1.0 Chromium)"},{"key":"webgl_aliased_line_width_range","value":"[1, 1]"},{"key":"webgl_aliased_point_size_range","value":"[1, 1024]"},{"key":"webgl_antialiasing","value":"yes"},{"key":"webgl_bits","value":"8,8,24,8,8,0"},{"key":"webgl_max_params","value":"16,32,16384,1024,16384,16,16384,30,16,16,4095"},{"key":"webgl_max_viewport_dims","value":"[32767, 32767]"},{"key":"webgl_unmasked_vendor","value":"Google Inc. (NVIDIA)"},{"key":"webgl_unmasked_renderer","value":"ANGLE (NVIDIA, NVIDIA GeForce RTX 3090 Ti Direct3D11 vs_5_0 ps_5_0, D3D11)"},{"key":"webgl_vsf_params","value":"23,127,127,23,127,127,23,127,127"},{"key":"webgl_vsi_params","value":"0,31,30,0,31,30,0,31,30"},{"key":"webgl_fsf_params","value":"23,127,127,23,127,127,23,127,127"},{"key":"webgl_fsi_params","value":"0,31,30,0,31,30,0,31,30"},{"key":"webgl_hash_webgl","value":"ff2121bc6f4faae22bb7a13a31f9e92d"},{"key":"user_agent_data_brands","value":"Chromium,Microsoft Edge,Not:A-Brand"},{"key":"user_agent_data_mobile","value":false},{"key":"navigator_connection_downlink","value":10.0},{"key":"navigator_connection_downlink_max","value":null},{"key":"network_info_rtt","value":100},{"key":"network_info_save_data","value":false},{"key":"network_info_rtt_type","value":null},{"key":"screen_pixel_depth","value":24},{"key":"navigator_device_memory","value":8},{"key":"navigator_languages","value":"en-US"},{"key":"window_inner_width","value":0},{"key":"window_inner_height","value":0},{"key":"window_outer_width","value":2212},{"key":"window_outer_height","value":797},{"key":"browser_detection_firefox","value":false},{"key":"browser_detection_brave","value":false},{"key":"audio_codecs","value":"{\"ogg\":\"probably\",\"mp3\":\"probably\",\"wav\":\"probably\",\"m4a\":\"maybe\",\"aac\":\"probably\"}"},{"key":"video_codecs","value":"{\"ogg\":\"probably\",\"h264\":\"probably\",\"webm\":\"probably\",\"mpeg4v\":\"\",\"mpeg4a\":\"\",\"theora\":\"\"}"},{"key":"media_query_dark_mode","value":true},{"key":"headless_browser_phantom","value":false},{"key":"headless_browser_selenium","value":false},{"key":"headless_browser_nightmare_js","value":false},{"key":"document__referrer","value":"https://www.roblox.com/"},{"key":"window__ancestor_origins","value":["https://www.roblox.com","https://www.roblox.com"]},{"key":"window__tree_index","value":[0,0]},{"key":"window__tree_structure","value":"[[[]]]"},{"key":"window__location_href","value":"https://client-api.arkoselabs.com/v2/A2A14B1D-1AF3-C791-9BBC-EE33CC7A0A6F/1.4.0/enforcement.86785498834e3af905f439f783c60e61.html"},{"key":"client_config__sitedata_location_href","value":"https://www.roblox.com/arkose/iframe"},{"key":"client_config__surl","value":"https://client-api.arkoselabs.com"},{"key":"mobile_sdk__is_sdk"},{"key":"client_config__language","value":null},{"key":"navigator_battery_charging","value":true},{"key":"audio_fingerprint","value":"124.04347527516074"}]},{"key":"fe","value":["DNT:unknown","L:en-US","D:24","PR:1","S:3440,1440","AS:3440,1392","TO:-420","SS:true","LS:true","IDB:true","B:false","ODB:true","CPUC:unknown","PK:Win32","CFP:1789402718","FR:false","FOS:false","FB:false","JSF:","P:Chrome PDF Viewer,Chromium PDF Viewer,Microsoft Edge PDF Viewer,PDF Viewer,WebKit built-in PDF","T:0,false,false","H:32","SWF:false"]},{"key":"ife_hash","value":"68cecd0b0988ca1d484f211670cd1f5e"},{"key":"cs","value":1},{"key":"jsbd","value":"{\"HL\":2,\"NCE\":true,\"DT\":\"\",\"NWD\":\"false\",\"DOTO\":1,\"DMTO\":1}"}],separators=(",", ":")),_UA+str(round(ms-(ms % 21600)))).encode()).decode()

# def Getbda():
#    return None

def Solve(text,data):
    for i in range(5): # max try
        try:
            id=Clicap.post("https://api.nopecha.com/",json={
                "key": _KEY,
                "type": "funcaptcha",
                "task": text,
                "image_data": [data]
            }).json()
            if id.get("error",0) != 0: sleep(0.5);continue
            for _ in range(15): # 15 sec
                resp=Clicap.get(f"https://api.nopecha.com/",params={"key":_KEY,"id":id["data"]}).json()
                if resp.get("data",0) != 0: return resp["data"]
                sleep(1)
            return [] # renew captcha
        except:pass# Exception as e:print("nopecha",e)

class FunCaptcha:
    def __init__(self,sitekey,proxies=None) -> None:
        self.Cli:Client=None
        self.Token:str=None
        self.TokenSess:str=None
        self.proxies=proxies
        self.sitekey=sitekey
        self.tier="30"
    def Request(self,method,url,data=None,json=None):
        time_=self.unix()
        for _ in range(5):
            try:return self.Cli.request(method,url,data=data,json=json,headers={"cookie":f"timestamp={time_}; __cf_bm=BSC;","x-requested-id":encrypt('{}',f"REQUESTED{self.TokenSess}ID"),"x-newrelic-timestamp":time_})
            except:sleep(1)
    def GetImage(self):
        pass
    def unix(self):
        a=str(int(float(datetime.now(tzlocal.get_localzone()).timestamp()*1e3)))
        return a[0:7]+"00"+a[7:]
    def Solve(self):
        self.Cli=Client(headers={
            "accept": "*/*",
            # "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US,en;q=0.9",
            "cache-control": "no-cache",
            # "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            # "cookie": "__cf_bm=NIu6ZNtQp4.loEyvCTbTMg_AF2w7EQFBjzLpq9.17f8-1671658854-0-ARBSy+Ol9pPaUNhVJAaZgNPtZhKbP+iwMy1OpGcEhSNuT2l7kwCrjdlAIuMH8c7OFvMLBxip0nfqGT1tT61I/DM=; timestamp=167165800898083",
            "origin":"https://roblox-api.arkoselabs.com",
            "referer":"https://roblox-api.arkoselabs.com/",
            # "sec-ch-ua": '"Not?A_Brand";v="8", "Chromium";v="108", "Microsoft Edge";v="108"',
            # "sec-ch-ua-mobile": "?0",
            # "sec-ch-ua-platform": '"Windows"',
            # "sec-fetch-dest": "empty",
            # "sec-fetch-mode": "cors",
            # "sec-fetch-site": "same-origin",
            "user-agent": _UA,
            # "x-newrelic-timestamp": "167165800898083",
            # "x-requested-id": "{"ct":"Qnj7EetCV/c3sYuybK3hJg==","iv":"f34247c0b8973c906b9b7d589be8276c","s":"c36e3881b5ce8e6b"}",
            "x-requested-with": "XMLHttpRequest",
        },verify=SSL()(),timeout=10) # ,proxies=self.proxies
        resp=self.Request("POST","https://roblox-api.arkoselabs.com/fc/gfct/",data={"token":self.TokenSess,"sid":"us-east-1","lang":"en","render_type":"canvas","analytics_tier":self.tier,"data[status]":"init"}).json()
        if resp.get("error",0) != 0:return False
        GameToken=resp["challengeID"]
        try:
            FindThing=resp["string_table"][f"3.instructions-{resp['game_data']['game_variant']}"]
        except:print("! ERROR",resp)
        encrypted_img=resp["game_data"]["customGUI"].get("encrypted_mode",False)
        api_breaker=resp["game_data"]["customGUI"].get("api_breaker",0)
        Answer=[]
        if encrypted_img:
            keyimg=self.Request("POST","https://roblox-api.arkoselabs.com/fc/ekey/",data={"sid":"us-east-1","session_token":self.TokenSess,"game_token":GameToken,}).json().get("decryption_key",0)
            if keyimg==0:return False
        print(f"[*] solve type : {FindThing} len : {len(resp['game_data']['customGUI']['_challenge_imgs'])}")
        # print(f"https://roblox-api.arkoselabs.com/fc/gc/?token={self.TokenSess}&r=us-east-1&lang=en&pk=A2A14B1D-1AF3-C791-9BBC-EE33CC7A0A6F&cdn_url=https%3A%2F%2Froblox-api.arkoselabs.com%2Fcdn%2Ffc")
        for url in resp["game_data"]["customGUI"]["_challenge_imgs"]:
            resp=Cliimg.get(url,headers={"referer":"https://roblox-api.arkoselabs.com/fc/assets/tile-game-ui/13.33.0/standard/index.html?meta=3"})
            if resp.status_code != 200:return False
            if encrypted_img: # if encrypted
                data=decrypt(resp.text,keyimg).decode()
                # Image.open(BytesIO(b64decode(data))).save("asd.png")
            else:
                data=b64encode(resp.content).decode()
            resp=Solve(FindThing,data)#["data"]
            # print(resp)
            if len(resp) == 0:return False
            Answer.append(pos(resp.index(True),api_breaker))
            resp=self.Request("POST","https://roblox-api.arkoselabs.com/fc/ca/",data={
                "sid":"us-east-1",
                "session_token":self.TokenSess,
                "game_token":GameToken,        
                "guess":encrypt(dumps(Answer),self.TokenSess),
                "analytics_tier":self.tier,
                "bio":"eyJtYmlvIjoiIiwidGJpbyI6IiIsImtiaW8iOiIifQ==", # fix this
            }).json()
            # if resp.status_code != 200:
            #     print(resp,self.Token,f"https://roblox-api.arkoselabs.com/fc/gc/?token={self.TokenSess}&r=us-east-1&lang=en&pk=A2A14B1D-1AF3-C791-9BBC-EE33CC7A0A6F&cdn_url=https%3A%2F%2Froblox-api.arkoselabs.com%2Fcdn%2Ffc")
            #     return False
            # resp=resp.json()
            # print(resp)
            if resp.get("solved",False):return True
            # timeout
            if resp.get("response",0) != "not answered":return False
            if encrypted_img:
                keyimg=resp["decryption_key"]
        return False
    def Do(self,blob):
        Clix=Client(proxies=self.proxies,verify=SSL()(),timeout=10,headers={"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8","Accept": "*/*","Origin": "https://www.roblox.com","Referer": "https://www.roblox.com/","Accept-Language": "en-US","Accept-Encoding": "gzip, deflate","user-agent": _UA})
        for _ in range(5):
            try:
                resp=Clix.post(f"https://roblox-api.arkoselabs.com/fc/gt2/public_key/{self.sitekey}",data={"bda":Getbda(),"public_key":self.sitekey,"site":"https://www.roblox.com","userbrowser":_UA,"language":"en","capi_version":"1.4.3","capi_mode":"inline","style_theme":"default","rnd":f"0.{randint(3100153120312819,90023570840000682)}","data[blob]":blob}).json()
                if resp.get("token",0) == 0:sleep(1);continue
                self.Token=resp["token"]
                self.TokenSess=self.Token.split("|")[0]
                break
            except Exception as e:print(e)
        for _ in range(5): # max try
            try:
                if self.Solve():break
            except:pass
        return self.Token