import base64
import os

folder_portraits = 'photos/to encode PORTRAIT'
folder_landscapes = 'photos/to encode LANDSCAPE'
end_folder_portraits = 'photos/portraits'
end_folder_landscapes = 'photos/landscapes'

def portraits():
    for i,file in enumerate(os.listdir(folder_portraits)):
        # print(f"File to encode: {file}")
        name = i
        with open(f'{folder_portraits}/{file}', 'rb') as f:
            data = f.read()
            encoded = base64.b64encode(data)
            encoded_str = encoded.decode('utf-8')
            # print(f"Encoded {file}:", encoded_str)
        with open('photos/examples/example photo.svg', 'r') as f:
            svg = f.read()
            svg = svg.replace('REPLACE_ME', encoded_str)
            with open(f'{end_folder_portraits}/{name}.svg', 'w') as f:
                f.write(svg)
        # break
def landscapes():
    for i in range(len(os.listdir(folder_landscapes))):
        print((i,(i+3%len(os.listdir(folder_landscapes)))))
        print(len(os.listdir(folder_landscapes)))
        left =i
        right = (i+3)%len(os.listdir(folder_landscapes))
        if left>right:
            left,right = right,left
        files_to_encode = os.listdir(folder_landscapes)[left:right]
        print(files_to_encode)
        # print(f"File to encode: {file}")
        encoded_list = []
        for file in files_to_encode:
            name = i
            with open(f'{folder_landscapes}/{file}', 'rb') as f:
                data = f.read()
                encoded = base64.b64encode(data)
                encoded_str = encoded.decode('utf-8')
                encoded_list.append(encoded_str)
        with open('photos/examples/example landscape.svg', 'r') as f:
            svg = f.read()
            svg = svg.replace('replace_1', encoded_list[0])
            svg = svg.replace('replace_2', encoded_list[1])
            svg = svg.replace('replace_3', encoded_list[2])

            with open(f'{end_folder_landscapes}/{name}.svg', 'w') as f:
                f.write(svg)
portraits()
landscapes()

