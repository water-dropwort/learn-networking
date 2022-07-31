# パラメータファイルクラス
import json

def export_default_json(filepath):
    fobj = None
    try:
        fobj = open(filepath, "w") # create or overwrite
        json.dump(Parameter.default_parameter_dictionary(), fobj)
    except Exception as ex:
        print("Failed to export file. Detail:",ex)
    finally:
        if fobj != None:
            fobj.close()

class Parameter:
    # Properties
    @property
    def host(self):
        return self.__host
    @property
    def port(self):
        return self.__port
    @property
    def debugmode(self):
        return self.__debugmode
    @property
    def close_from_client(self):
        return self.__close_from_client

    # set value to private variants
    def __setparameter(self, param_dict):
        self.__host = param_dict["host"]
        self.__port = param_dict["port"]
        self.__debugmode = param_dict["debugmode"]
        self.__close_from_client = param_dict["close_from_client"]

    @staticmethod
    def default_parameter_dictionary():
        return { "host":"example.com",
                 "port":80,
                 "debugmode":False,
                 "close_from_client":False}

    # constructor
    # ファイルパス未指定か読み込みに失敗した場合はデフォルト値をセットする。
    def __init__(self, filepath = None):
        self.__setparameter(Parameter.default_parameter_dictionary())

        fobj = None
        try:
            if filepath == None:
                return
            fobj = open(filepath,"r")
            json_dict = json.load(fobj)
            self.__setparameter(json_dict)
        except Exception as ex:
            print("Failed to load parameter file. Detail:",ex)
            self.__setparameter(Parameter.default_parameter())
        finally:
            if fobj != None:
                fobj.close()
