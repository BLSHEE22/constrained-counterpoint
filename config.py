# run config

CF_LENGTH = 11
SCALE = "Major"
INSTRUMENT = "harpsichord"

scales = {"Major": [-5,-3,-1,0,2,4,5,7,9,11,12,14,16], "Minor":[-5,-4,-1,0,2,3,5,7,8,10,12,14,15]}

majScales = {0:{0:"c",1:"des",2:"d",3:"ees",4:"e",5:"f",6:"fis",7:"g",8:"aes",9:"a",10:"bes",11:"b"},
                1:{0:"c",1:"des",2:"d",3:"ees",4:"e",5:"f",6:"ges",7:"g",8:"aes",9:"a",10:"bes",11:"b"},
                2:{0:"c",1:"cis",2:"d",3:"dis",4:"e",5:"f",6:"fis",7:"g",8:"gis",9:"a",10:"ais",11:"b"},
                3:{0:"c",1:"des",2:"d",3:"ees",4:"e",5:"f",6:"fis",7:"g",8:"aes",9:"a",10:"bes",11:"b"},
                4:{0:"c",1:"cis",2:"d",3:"dis",4:"e",5:"f",6:"fis",7:"g",8:"gis",9:"a",10:"ais",11:"b"},
                5:{0:"c",1:"des",2:"d",3:"ees",4:"e",5:"f",6:"ges",7:"g",8:"aes",9:"a",10:"bes",11:"b"},
                6:{0:"c",1:"cis",2:"d",3:"dis",4:"e",5:"eis",6:"fis",7:"g",8:"gis",9:"a",10:"ais",11:"b"},
                7:{0:"c",1:"cis",2:"d",3:"dis",4:"e",5:"f",6:"fis",7:"g",8:"gis",9:"a",10:"ais",11:"b"},
                8:{0:"c",1:"des",2:"d",3:"ees",4:"e",5:"f",6:"ges",7:"g",8:"aes",9:"a",10:"bes",11:"b"},
                9:{0:"c",1:"cis",2:"d",3:"dis",4:"e",5:"f",6:"fis",7:"g",8:"gis",9:"a",10:"ais",11:"b"},
                10:{0:"c",1:"des",2:"d",3:"ees",4:"e",5:"f",6:"ges",7:"g",8:"aes",9:"a",10:"bes",11:"b"},
                11:{0:"c",1:"cis",2:"d",3:"dis",4:"e",5:"f",6:"fis",7:"g",8:"gis",9:"a",10:"ais",11:"b"},} 

scaleStartTrans = {"c":"C","cis":"C#","des":"D-Flat","d":"D","dis":"D#","ees":"E-Flat","e":"E",
                           "fes":"F-Flat","f":"F","fis":"F#","ges":"G-Flat","g":"G","gis":"G#",
                           "aes":"A-Flat","a":"A","ais":"A#","bes":"B-Flat","b":"B","ces":"C-Flat"}

interval_dict = {0: "P8",
                     1: "m2",
                     2: "M2",
                     3: "m3",
                     4: "M3",
                     5: "P4",
                     6: "b5",
                     7: "P5",
                     8: "m6",
                     9: "M6",
                     10: "m7",
                     11: "M7"}

disallowed_parallel_intervals = [0, 5, 6, 7, 10, 11]