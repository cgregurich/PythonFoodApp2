
class FoodItem:
    def __init__(self, info_dict=None):
        self.info = {'name': None, 'ss': None, 'unit': None, 'cal': None, 'carb': None, 'fat': None, 'protein': None,
                     'fiber': None, 'sugar': None}
        if not info_dict:
            self.info = {'name': None, 'ss': None, 'unit': None, 'cal': None, 'carb': None, 'fat': None, 'protein': None, 'fiber': None, 'sugar': None}
        else:
            for key in self.info.keys():
                self.info[key] = info_dict[key]
            self.numberize_info()


    def __str__(self):
        return_str = ''
        for key, value in self.info.items():
            return_str += f"{key}:{value} "
        return return_str.strip()

    def set_info(self, info_dict):
        self.info = info_dict

    def set_info_from_string_list(self, info_list):
        i = 0
        for key in self.info.keys():
            self.info[key] = info_list[i]
            i += 1 
        self.numberize_info()
            
    def numberize_info(self):
        """Ensures that all number information of the FoodItem is indeed a number (float or int, instead of str)
        This is more or less a helper method for set_info_from_string_list"""
        for key in self.info.keys():
            if key != 'name' and key != 'unit':
                try:
                    self.info[key] = float(self.info[key])
                except ValueError:
                    return False
                if self.info[key] == int(self.info[key]):
                    self.info[key] = int(self.info[key])
        self.info['cal'] = round(self.info['cal'])
        return True

    def is_missing_info(self):
        for value in self.info.values():
            if value is None or value == "":
                return True
        return False
            
        

    def set_info_from_tuple(self, info_tup):
        i = 0
        for key in self.info.keys():
            self.info[key] = info_tup[i]
            i += 1
        self.numberize_info()

    def proportionalize(self, amount):
        if self.is_missing_info():
            raise TypeError('Food is missing info')

        if int(amount) == amount:
            amount = int(amount)

        ratio = amount / self.info['ss']
        for key, value in self.info.items():
            if key == 'ss':

                self.info[key] = amount
            elif key != 'name' and key != 'unit':
                new_val = self.info[key] * ratio
                if new_val.is_integer():
                    new_val = int(new_val)
                else:
                    new_val = round(new_val, 1)
                self.info[key] = new_val

    


    def get_tuple(self):
        return tuple(self.info.values())

    def is_info_same(self, other_food):
        for key in self.info.keys():
            if self.info[key] != other_food.info[key]:
                return False
        return True



    @property
    def name(self):
        return self.info['name']

    @property
    def ss(self):
        return self.info['ss']

    @property
    def unit(self):
        return self.info['unit']

    @property
    def cal(self):
        return self.info['cal']

    @property
    def carb(self):
        return self.info['carb']

    @property
    def fat(self):
        return self.info['fat']

    @property
    def protein(self):
        return self.info['protein']

    @property
    def fiber(self):
        return self.info['fiber']

    @property
    def sugar(self):
        return self.info['sugar']



