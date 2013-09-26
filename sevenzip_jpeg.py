def Make7zip(In, Out, Password=None):
    import subprocess
    from os import remove, path
    cmd = ['7za', 'a', Out, In, '-mx1', '-t7z', '-y']
    if Password is not None and len(Password) > 0:
        cmd.append('-p' + Password)
        cmd.append('-mhe')

    print(cmd.__str__())

    if path.exists(Out):
        remove(Out)
    sp = subprocess.Popen(cmd, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
    out, err = sp.communicate()
    return out
def AppendToJpeg(Img, SrcFile, Dest):
    from shutil import copyfile
    if Img != Dest:
        copyfile(Img, Dest)
    ImgOut = file(Dest, "ab")
    ImgOut.write(open(SrcFile, "rb").read())
    ImgOut.close()

def Make7zJpeg(Source, ImgSource, Dest, Password=None):
    import tempfile, os
    out = ""
    if os.path.splitext(Source)[1] != '7z':
        temp7z, temp7zname = tempfile.mkstemp(suffix='.7z')
        os.close(temp7z)
        out = Make7zip(Source, temp7zname, Password)
        AppendToJpeg(ImgSource, temp7zname, Dest)
        os.remove(temp7zname)
    else:
        AppendToJpeg(ImgSource, Source, Dest)

    return out