from workhub.user_profile.service import service_get_detail,service_update_detail
from workhub.user_profile.schema import UpdateUserDetail
from langchain.tools import tool
def get_user_tools(db,current_user) :
    @tool
    async  def get_profile_detail() :
        return await service_get_detail(current_user=current_user,db =db)
    @tool(args_schema=UpdateUserDetail)
    async def update_profile_detail(name,email_id,mobile_no,gender) :
        request = UpdateUserDetail(name=name,email=email_id,mobile_no=mobile_no,gender = gender)
        return await service_update_detail(current_user=current_user,db =db,request = request)