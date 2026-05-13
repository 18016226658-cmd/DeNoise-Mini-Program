import openai
import os
def chatGPTTest(question):
    # 指定 OpenAI API 的密钥
    # openai.api_key = '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'
    try:
        print(" 1 ===========================")
        # openai.api_key = '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'
        # openai.api_key ='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'
        openai.api_key ='sk-mG09gWgSCt0J7rT-KIPmC312awJ-QPJ-Fj9sEARXAwT3BlbkFJkYQBy1RWbAbuySA7ll0tUSz7-VBMcwUIoRFUVz4z0A'

        os.environ["HTTP_PROXY"] = "http://127.0.0.1:33210"
        os.environ["HTTPS_PROXY"] = "http://127.0.0.1:33210"

        # q= [{"role": "user", "content": "你好"}]
        q = [{"role": "user", "content": question}]

        print(" 2 ===========================")

        rsp = openai.ChatCompletion.create(
          model="gpt-3.5-turbo",      # 只能用这个模型
          # model="gpt-3.5-turbo-0301",   #这个模型已经不能用 会保存
          messages=q
        )
        print(" 3 ===========================")
        msg = rsp.get("choices")[0]["message"]["content"]
        print(" 4 ===========================")

    except:
        # print(" 5 ===========================")
        msg ="调用openAI出错，不能为你提供chat服务！"
    print(msg)
    # return msg

chatGPTTest("苏州在哪里")




#
# import openai
# import os
# try:
#     openai.api_key ='sk-mG09gWgSCt0J7rT-KIPmC312awJ-QPJ-Fj9sEARXAwT3BlbkFJkYQBy1RWbAbuySA7ll0tUSz7-VBMcwUIoRFUVz4z0A'
#     os.environ["HTTP_PROXY"] = "http://127.0.0.1:33210"
#     os.environ["HTTPS_PROXY"] = "http://127.0.0.1:33210"
#     q= [{"role": "user", "content": "苏州在哪里"}]
#     rsp = openai.ChatCompletion.create(
#       model= "gpt-3.5-turbo",
#       temperature =1 ,
#       max_tokens =1024 ,
#       messages=q,
#       # stream=True
#     )
#     msg = ''
#     print(rsp)
#     # for i in rsp:
#     #     print(i)
#     #     try:
#     #         # msg += i["choices"][0]["message"]["content"]
#     #         msg += i["choices"][0]["delta"]["content"]
#     #     except Exception as e:
#     #         print("===========================")
#     #
#     #         msg = f"调用openAI出错：{e}"
#     #         print(msg)
#     #         break
#     msg = rsp.get("choices")[0]["message"]["content"]
# except Exception as e:
#     msg = f"调用openAI出错：{e}"
# print(msg)
#




























# import os
# def chatGPT(question):
#     # 指定 OpenAI API 的密钥
#     # openai.api_key = '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'
#     try:
#         # openai.api_key = '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'
#
#         print(" 1 ===========================")
#         # openai.api_key = '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'
#         # openai.api_key ='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'
#         openai.api_key ='sk-mG09gWgSCt0J7rT-KIPmC312awJ-QPJ-Fj9sEARXAwT3BlbkFJkYQBy1RWbAbuySA7ll0tUSz7-VBMcwUIoRFUVz4z0A'
#
#         os.environ["HTTP_PROXY"] = "http://127.0.0.1:33210"
#         os.environ["HTTPS_PROXY"] = "http://127.0.0.1:33210"
#
#         # q= [{"role": "user", "content": "你好"}]
#         q = [{"role": "user", "content": question}]
#
#         print(" 2 ===========================")
#
#         rsp = openai.ChatCompletion.create(
#           model="gpt-3.5-turbo-0301",
#           messages=q
#         )
#         print(" 3 ===========================")
#         msg = rsp.get("choices")[0]["message"]["content"]
#         print(" 4 ===========================")
#
#     except:
#         # print(" 5 ===========================")
#         msg ="调用openAI出错，不能为你提供chat服务！"
#     print(msg)
#     # return msg

# chatGPT("苏州在哪里")