import os
import sys
import filecmp
import shutil
import __main__


python = sys.executable


extentions_folder = os.path.join(os.path.dirname(os.path.realpath(__main__.__file__)),
                                 "web" + os.sep + "extensions" + os.sep + "Gemini_Zho")
javascript_folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), "js")

if not os.path.exists(extentions_folder):
    print('Making the "web\extensions\Gemini_Zho" folder')
    os.mkdir(extentions_folder)

result = filecmp.dircmp(javascript_folder, extentions_folder)

if result.left_only or result.diff_files:
    print('Update to javascripts files detected')
    file_list = list(result.left_only)
    file_list.extend(x for x in result.diff_files if x not in file_list)

    for file in file_list:
        print(f'Copying {file} to extensions folder')
        src_file = os.path.join(javascript_folder, file)
        dst_file = os.path.join(extentions_folder, file)
        if os.path.exists(dst_file):
            os.remove(dst_file)
        #print("disabled")
        shutil.copy(src_file, dst_file)


from .GeminiAPINode import NODE_CLASS_MAPPINGS as NODE_CLASS_MAPPINGS_G

# Combine the dictionaries
NODE_CLASS_MAPPINGS = {**NODE_CLASS_MAPPINGS_G}

__all__ = ['NODE_CLASS_MAPPINGS']
