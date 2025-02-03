_F='connector_id'
_E='Invalid chart type. Use an ID found in the DataFrame get_plot_types()'
_D='100%'
_C='api_service'
_B='widget_id'
_A=None
import os,json,uuid,urllib.parse
from IPython.core.display import display,HTML
import warnings
warnings.filterwarnings('ignore',message='Consider using IPython.display.IFrame instead',category=UserWarning)
from datetime import datetime,timedelta
import pytz
UTC=pytz.utc
from project.models import UserProfile,PlotDBChart,PlotDBChartShared,PlotDBPermission
from project.sparta_1d1c5d5897.sparta_f2e5918cc6.qube_56e2b853b1 import sparta_c8186175d6
from project.sparta_1d1c5d5897.sparta_e0f10cf586.qube_97c853e9c9 import convert_to_dataframe,convert_dataframe_to_json
from project.sparta_1d1c5d5897.sparta_e0f10cf586.qube_da7a8a8853 import sparta_e061501b2d
class Spartaqube:
	_instance=_A
	def __new__(A,*B,**C):
		if A._instance is _A:A._instance=super().__new__(A);A._instance._initialized=False
		return A._instance
	def __init__(A,api_token_id=_A):
		B=api_token_id
		if A._initialized:return
		A._initialized=True
		if B is _A:
			try:B=os.environ['api_key']
			except:pass
		A.api_token_id=B;A.user_obj=UserProfile.objects.get(api_key=B).user
	def test(A):print('test')
	def sparta_3b7a0f2b59(A,widget_id):B={_C:'get_widget_data',_B:widget_id};return sparta_c8186175d6(B,A.user_obj)
	def sparta_06e86aa22f(A,widget_id):B={_C:'has_widget_id',_B:widget_id};return sparta_c8186175d6(B,A.user_obj)
	def get_widget(C,widget_id,width=_D,height=500):
		A=PlotDBChartShared.objects.filter(is_delete=0,user=C.user_obj,plot_db_chart__is_delete=0,plot_db_chart__plot_chart_id=widget_id)
		if A.count()>0:B=str(uuid.uuid4());D=datetime.now().astimezone(UTC);PlotDBPermission.objects.create(plot_db_chart=A[0].plot_db_chart,token=B,date_created=D);return HTML(f'<iframe src="/plot-widget-token/{B}" width="{width}" height="{height}" frameborder="0" allow="clipboard-write"></iframe>')
		return'You do not have the rights to access this object'
	def iplot(I,*B,width=_D,height=550):
		if len(B)==0:raise Exception('You must pass at least one input variable to plot')
		else:
			C=dict()
			for(E,D)in enumerate(B):
				if D is _A:continue
				F=convert_to_dataframe(D);C[E]=convert_dataframe_to_json(F)
			G=json.dumps(C);A=str(uuid.uuid4());H=f'''
                <form id="dataForm_{A}" action="plot-gui" method="POST" target="{A}">
                    <input type="hidden" name="data" value=\'{G}\' />
                </form>
                <iframe 
                    id="{A}"
                    name="{A}"
                    width="{width}" 
                    height="{height}" 
                    frameborder="0" 
                    allow="clipboard-write"></iframe>

                <script>
                    // Submit the form automatically to send data to the iframe
                    document.getElementById(\'dataForm_{A}\').submit();
                </script>
                ''';return HTML(H)
	def plot(V,*W,**A):
		I='width';H='chart_type';D=dict()
		for(J,F)in A.items():
			if F is _A:continue
			K=convert_to_dataframe(F);D[J]=convert_dataframe_to_json(K)
		E=_A
		if H not in A:
			if _B not in A:raise Exception("Missing chart_type parameter. For instance: chart_type='line'")
			else:E=0
		if E is _A:
			L=sparta_e061501b2d(b_return_type_id=True)
			try:M=json.loads(D[H])['data'][0][0];E=[A for A in L if A['ID']==M][0]['type_plot']
			except:raise Exception(_E)
		N=A.get(I,_D);O=A.get(I,'500');P=A.get('interactive',True);G=A.get(_B,_A);Q={'interactive_api':1 if P else 0,'is_api_template':1 if G is not _A else 0,_B:G};R=json.dumps(Q);S=urllib.parse.quote(R);B=dict();B['res']=1;B['notebook_variables']=D;B['type_chart']=E;B['override_options']=D.get('options',dict());T=json.dumps(B);C=str(uuid.uuid4());U=f'''
            <form id="dataForm_{C}" action="plot-api/{S}" method="POST" target="{C}">
                <input type="hidden" name="data" value=\'{T}\' />
            </form>
            <iframe 
                id="{C}"
                name="{C}"
                width="{N}" 
                height="{O}" 
                frameborder="0" 
                allow="clipboard-write"></iframe>

            <script>
                // Submit the form automatically to send data to the iframe
                document.getElementById(\'dataForm_{C}\').submit();
            </script>
            ''';return HTML(U)
	def plot_documentation(B,chart_type='line'):
		A=chart_type;C=B.get_plot_types()
		if len([B for B in C if B['ID']==A])>0:D=f"api#plot-{A}";return D
		else:raise Exception(_E)
	def sparta_f0a8b18a10(B,*C,**A):
		if _B in A:return B.plot(*C,**A)
		raise Exception('Missing widget_id')
	def sparta_966c0b9ab6(A,connector_id):B={_C:'get_connector_tables',_F:connector_id};return sparta_c8186175d6(B,A.user_obj)
	def sparta_0a3b98f9f8(C,connector_id,table=_A,sql_query=_A,output_format=_A):B=sql_query;A={_C:'get_data_from_connector'};A[_F]=connector_id;A['table_name']=table;A['query_filter']=B;A['bApplyFilter']=1 if B is not _A else 0;return sparta_c8186175d6(A,C.user_obj)
	def apply_method(B,method_name,*D,**C):A=C;A[_C]=method_name;return sparta_c8186175d6(A,B.user_obj)
	def __getattr__(A,name):return lambda*B,**C:A.apply_method(name,*B,**C)