from enum import Enum

class SymbolTable:
    def __init__(self):
        self.subroutine_scope = {}
        self.class_scope = {}
        self.kind_index = {
            "var": 0,
            "arg": 0,
            "field": 0,
            "static": 0
        }

    def start_subroutine(self):
        self.subroutine_scope = {}
        self.kind_index["var"] = 0
        self.kind_index["arg"] = 0
        
    def define(self, iden_name, iden_type, iden_kind):
        class_scope_kinds = ["field", "static"]
        subroutine_scope_kinds = ["var", "arg"]

        curr_index = self.kind_index[iden_kind]
        if iden_kind in class_scope_kinds:
            self.class_scope[iden_name] = {
                "iden_type": iden_type,
                "iden_kind": iden_kind,
                "iden_index": curr_index
            }
        elif iden_kind in subroutine_scope_kinds:
            self.subroutine_scope[iden_name] = {
                "iden_type": iden_type,
                "iden_kind": iden_kind,
                "iden_index": curr_index
            }
        self.kind_index[iden_kind] = curr_index + 1

    def var_count(self, iden_kind):
       return self.kind_index[iden_kind] 

    def kind_of(self, iden_name):
        if iden_name in self.subroutine_scope:
            return self.subroutine_scope[iden_name]["iden_kind"]
        if iden_name in self.class_scope:
            return self.class_scope[iden_name]["iden_kind"]
    
    def type_of(self, iden_name):
        if iden_name in self.subroutine_scope:
            return self.subroutine_scope[iden_name]["iden_type"]
        if iden_name in self.class_scope:
            return self.class_scope[iden_name]["iden_type"]

    def index_of(self, iden_name):
        if iden_name in self.subroutine_scope:
            return self.subroutine_scope[iden_name]["iden_index"]
        if iden_name in self.class_scope:
            return self.class_scope[iden_name]["iden_index"]

    def print_xml(self, iden_name):
        print("<identifierInfo>")
        print("  <kind> {} </kind>".format(self.kind_of(iden_name)))
        print("  <type> {} </type>".format(self.type_of(iden_name)))
        print("  <index> {} </index>".format(self.index_of(iden_name)))
        print("</identifierInfo>")

