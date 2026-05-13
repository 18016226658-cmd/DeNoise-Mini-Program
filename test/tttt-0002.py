
@app.route('/api/CreateJar', methods=[ 'POST'])
def CreateJar():
    import subprocess
    # 接受表单上用户输入的内容（Myclass文件路径，Jar路径、java文件路径）
    Myclass_path = request.form.get("Myclass_path")
    FileName_txt = request.form.get("FileName_txt")
    FileName_jar = request.form.get("FileName_jar")
    FileName_java1 = request.form.get("FileName_java")
    FileName_java = "D:/WxMinPro/java/" + FileName_java1

    # （1）下面为 键盘输入 打的包完整的主类名称，如：com.example.JpypeDemo
    text1 = "com.example.JpypeDemo"
    text2 = "Main-Class: " + text1
    print("你要打成jar包的完整的主类名称为：" + text2)

    # （2）将打包主类配置文件写入 FileName指定是文件中
    file = open(FileName_txt, 'w')
    file.write(text2)

    # （3）将java文件 编译为 class字节文件
    subprocess.call(['javac.exe', '-encoding', 'UTF-8', '-d', Myclass_path, FileName_java])

    # （4）将当前的 myclass_path 下 com 根类下的 class文件 打为 jar包文件
    subprocess.call(['jar.exe', '-cvfm', FileName_jar, FileName_txt, 'com'])
    msg = "打包成功！"
    return msg




  # 1.获取jvm.dll 的文件路径
    jvmPath = jp.getDefaultJVMPath()

    # 2.开启jvm
    jp.startJVM(jvmPath, "-ea", "-Djava.class.path=%s" % (jarpath))

    # 3.加载java类（参数是java的长类名）
    JDClass = jp.JClass("com.example.JpypeDemo")

    # 4.实例化java对象
    jd = JDClass()

    # 5.调用java方法，由于是静态方法，直接使用类名就可以调用方法
    sumAdd = jd.Add(int(Data1), int(Data2))
    sumSub = jd.Sub(int(Data1), int(Data2))



    @app.route('/api/CompileFile', methods=['GET', 'POST'])
    def CompileFile():
        import subprocess
        Fpath = request.args.get("file")

        File_gcc = r'C:/soft/Dev-Cpp-5.15/TDM-GCC-64/bin/gcc.exe'
        File_so = 'D:/WxMinPro/static/receive/c/libpycall.so'
        File_c = 'D:/WxMinPro/static/receive/c/Test.c'

        subprocess.call([File_gcc, '-o', File_so, '-shared', '-fPIC', File_c])

        return '0'
