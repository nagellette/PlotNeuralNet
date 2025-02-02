
import sys
sys.path.append('../')
from pycore.tikzeng import *
from pycore.blocks  import *

arch = [ 
    to_head('..'), 
    to_cor(),
    to_begin(),

    custom_Satellite( name="satellite1", s_filer=572, n_filer=13, offset="(0,0,0)", to="(0,0,0)", width=3, height=40, depth=40, opacity = 1.0 ),
    custom_Trajectory( name="trajectory1", s_filer=572, n_filer=7, offset="(0,0,0)", to="(satellite1-east)", width=1.5, height=40, depth=40, opacity = 1.0),


    #block-001
    to_ConvConvRelu( name='ccr_b1', s_filer=572, n_filer=(20,20), offset="(3,0,0)", to="(trajectory1-east)", width=(4.5,4.5), height=40, depth=40, opacity=1.0, caption="2 x Conv" ),
    to_connection("trajectory1", "ccr_b1"),
    to_Pool( name="pool_b1", offset="(1,0,0)", to="(ccr_b1-east)", width=1, height=32, depth=32, opacity=1.0, caption="Pool" ),
    
    *block_2ConvPool( name='b2', botton='pool_b1', top='pool_b2', s_filer=256, n_filer=128, offset="(1,0,0)", size=(32,32,3.5), opacity=1.0 ),
    *block_2ConvPool( name='b3', botton='pool_b2', top='pool_b3', s_filer=128, n_filer=256, offset="(1,0,0)", size=(25,25,4.5), opacity=1.0 ),
    *block_2ConvPool( name='b4', botton='pool_b3', top='pool_b4', s_filer=64,  n_filer=512, offset="(1,0,0)", size=(16,16,5.5), opacity=1.0 ),

    #Bottleneck
    #block-005
    to_ConvConvRelu( name='ccr_b5', s_filer=35, n_filer=(512,512), offset="(2,0,0)", to="(pool_b4-east)", width=(8,8), height=8, depth=8, caption="Bottleneck", opacity=1.0  ),
    to_connection( "pool_b4", "ccr_b5"),

    #Decoder
    *block_Unconv( name="b6", botton="ccr_b5", top='end_b6', s_filer=64,  n_filer=512, offset="(2.1,0,0)", size=(16,16,5.0), opacity=1.0 ),
    to_skip( of='ccr_b4', to='ccr_res_b6', pos=1.25),
    *block_Unconv( name="b7", botton="end_b6", top='end_b7', s_filer=128, n_filer=256, offset="(2.1,0,0)", size=(25,25,4.5), opacity=1.0 ),
    to_skip( of='ccr_b3', to='ccr_res_b7', pos=1.25),    
    *block_Unconv( name="b8", botton="end_b7", top='end_b8', s_filer=256, n_filer=128, offset="(2.1,0,0)", size=(32,32,3.5), opacity=1.0 ),
    to_skip( of='ccr_b2', to='ccr_res_b8', pos=1.25),    
    
    *block_Unconv( name="b9", botton="end_b8", top='end_b9', s_filer=512, n_filer=64,  offset="(2.1,0,0)", size=(40,40,2.5), opacity=1.0 ),
    to_skip(of='ccr_b1', to='ccr_res_b9', pos=1.25),
    
    to_ConvSoftMax( name="soft1", s_filer=512, offset="(0.75,0,0)", to="(end_b9-east)", width=1, height=40, depth=40, caption="SOFT", opacity=1.0 ),
    to_connection( "end_b9", "soft1"),
     
    to_end() 
    ]


def main():
    namefile = str(sys.argv[0]).split('.')[0]
    to_generate(arch, namefile + '.tex' )

if __name__ == '__main__':
    main()
    
