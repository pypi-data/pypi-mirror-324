"""A test package"""


import os 
import torch

class Hooks():
    
    

    def __init__(self,model_object:object,layer_index=None):
        
        self.object=model_object
        self.layer_index=layer_index
        self.layers=list(self.object.children())
        
 
        self.iteration_idx_fbph=0
        self.new_values_output_fbph=None
        self.noise_output_fbph=None
        
        
        self.iteration_idx_fbh=0
        self.noise_input_fbh=None
        self.new_values_input_fbh=None
        
        
        self.iteration_idx_fph=0
        self.noise_input_fph=None
        self.new_values_input_fph=None
        
        
        self.iteration_idx_fh=0
        self.noise_output_fh=None
        self.new_values_output_fh=None
        
       
        
    def get_shape_of_layer(self):
        IN,OUT=self.layers[self.layer_index].in_features,self.layers[self.layer_index].out_features
        
        print("SHAPE OF LAYER IS : ",IN,OUT)
        return IN,OUT
    
    
   


    def visualize_forward_hook_function(self,module,inputs, outputs):
        print("VISUALIZING FH ITERATION INDEX : ",self.iteration_idx_fh)

        
        BATCH_SIZE=inputs[0].shape[0]
        dir_name="saved_forward_hook_values"
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
            print(f"DIRECTORY {dir_name} CREATED.")
        else:
            print(f"DIRECTORY {dir_name} ALREADY EXISTS.")
            

        
        print("STARTING TO SAVE THE FH VALUES")
        
        if inputs!=None and inputs[0]!=None:
            save_batch_tensors_input=inputs[0]
            

            
            
            torch.save(save_batch_tensors_input, f'{dir_name}/input_{self.iteration_idx_fh}_batch_size_{BATCH_SIZE}_layer_{self.layer_index}_forward_hook_tensor.pt')
            
            print("SAVED THE FH INPUTS..")
        elif inputs==None or inputs[0]==None:
            print("INPUTS FH CANNOT BE SAVED SINCE THEY ARE NULL...")
            
            
            
            
        if outputs!=None:
            save_batch_tensors_output=outputs
            

            torch.save(save_batch_tensors_output, f'{dir_name}/output_{self.iteration_idx_fh}_batch_size_{BATCH_SIZE}_layer_{self.layer_index}_forward_hook_tensor.pt')
            
            print("SAVED THE FH OUTPUTS..")
        elif outputs==None:
            print("OUTPUTS FH CANNOT BE SAVED SINCE THEY ARE NULL...")
        self.iteration_idx_fh+=1
        
        print()
        return outputs
    
    
    def forward_hook_function(self,module,inputs,output):
        if output==None :
            print("TO BE RETURNED VALUE IS NONE . CHANGES CANNOT BE DONE , RETURNING ......")
            return 
       
        
        new_output=output
       
        
        if self.noise_output_fh==None and self.new_values_output_fh==None:
            print("NEITHER NOISE NOR NEW VALUES WERE PROVIDED FOR OUTPUTS TO BE UPGRADED FOR FH , RETURNING OLD VALUES .....")
            return new_output
        
        
        if self.new_values_output_fh==None:
            print("NEW VALUES NOT PROVIDED IN FH SO UPDATING WITH OLD VALUES")

         
        elif self.new_values_output_fh!=None:
            new_output=self.new_values_output_fh
            print("NEW VALUES PROVIDED IN FH SO UPDATING WITH NEW VALUES")
        
        if self.noise_output_fh==None:
            print("NOISE NOT PROVIDED IN FH SO UPDATING WITH 1")
            print()
            return new_output*1
            
        elif self.noise_output_fh!=None:
            print("NOISE PROVIDED IN FH SO UPDATING ")
            print()
            return new_output*self.noise_output_fh

        
            
        
        
    
    
    
    def register_fh(self,update=False,visualize=False,add_noise_output=False,add_values_output=False,noise_output=None,new_values_output=None):
        if update==False and visualize==False:
            print("YOU CAN VISUALIZE OR UPDATE")
            return
        if update==True:
            if add_noise_output==True:
                self.noise_output_fh=noise_output
            if add_values_output==True:
                self.new_values_output_fh=new_values_output


            return self.layers[self.layer_index].register_forward_hook(self.forward_hook_function)
        elif visualize==True:
            return self.layers[self.layer_index].register_forward_hook(self.visualize_forward_hook_function)
    
    
    
    
    
    
    
    
    
    
    
    
    def visualize_foward_pre_hook(self,module,inputs):
        
        
        
        print("VISUALIZING FPH ITERATION INDEX : ",self.iteration_idx_fph)
        BATCH_SIZE=inputs[0].shape[0]
        dir_name="saved_forward_prehook_inputs"
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
            print(f"DIRECTORY {dir_name} CREATED.")
        else:
            print(f"DIRECTORY {dir_name} ALREADY EXISTS.")
        print("STARTING TO SAVE THE FPH INPUTS")
        
        
        if inputs!=None and inputs[0]!=None:
            save_batch_tensors_input=inputs[0]

            torch.save(save_batch_tensors_input, f'{dir_name}/inputs_{self.iteration_idx_fph}_batch_size_{BATCH_SIZE}_layer_{self.layer_index}_forward_prehook_tensor.pt')
            
            print("SAVED THE FPH INPUTS...")
        elif inputs==None or inputs[0]==None:
            print("INPUTS FPH CANNOT BE SAVED SINCE THEY ARE NULL...")
        self.iteration_idx_fph+=1
        
        print()
        
        

        return inputs
    
    
    def forward_pre_hook_function(self,module,inputs):
        if inputs==None or inputs[0]==None:
            print("TO BE RETURNED VALUE IS NONE . CHANGES CANNOT BE DONE , RETURNING ......")
            return 
        
  
        new_fph_input=inputs[0]
    
        
       
        
        if self.noise_input_fph==None and self.new_values_input_fph==None:
            print("NEITHER NOISE NOR NEW VALUES WERE PROVIDED FOR FPH , RETURNING OLD VALUES .....")
            return (new_fph_input,)
        
        
        if self.new_values_input_fph==None:
            print("NEW VALUES NOT PROVIDED IN FPH SO UPDATING WITH OLD VALUES")

         
        elif self.new_values_input_fph!=None:
            new_fph_input=self.new_values_input_fph
            print("NEW VALUES PROVIDED IN FPH SO UPDATING WITH NEW VALUES")
        
        if self.noise_input_fph==None:
            print("NOISE NOT PROVIDED IN FPH SO UPDATING WITH 1")
            print()
            return (new_fph_input*1,)
           
            
        elif self.noise_input_fph!=None:
            print("NOISE PROVIDED IN FPH SO UPDATING ")
            print()
            return (new_fph_input*self.noise_input_fph,)
          

        
            
        
        
       
    
    
    
    
    
    
    def register_fph(self,update=False,visualize=False,add_noise_input=False,add_values_input=False,noise_input=None,new_values_input=None):
        if update==False and visualize==False:
            print("YOU CAN VISUALIZE OR UPDATE")
            return
        
        
        
        if update==True:
            if add_noise_input==True:
                self.noise_input_fph=noise_input
            if add_values_input==True:
                self.new_values_input_fph=new_values_input


            return self.layers[self.layer_index].register_forward_pre_hook(self.forward_pre_hook_function)
        elif visualize==True:
            return self.layers[self.layer_index].register_forward_pre_hook(self.visualize_foward_pre_hook)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    def visualize_full_backward_hook_function(self,module,grad_input, grad_output):
        print("VISUALIZING FBH ITERATION INDEX : ",self.iteration_idx_fbh)

        BATCH_SIZE=grad_output[0].shape[0]
        dir_name="saved_full_backward_hook_gradients"
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
            print(f"DIRECTORY {dir_name} CREATED.")
        else:
            print(f"DIRECTORY {dir_name} ALREADY EXISTS.")
            

        
        print("STARTING TO SAVE THE FBH GRADIENTS")
        
        if grad_input!=None and grad_input[0]!=None:
        
            save_batch_tensors_grad_input=grad_input[0]
            torch.save(save_batch_tensors_grad_input, f'{dir_name}/grad_input_{self.iteration_idx_fbh}_batch_size_{BATCH_SIZE}_layer_{self.layer_index}_full_backward_hook_tensor.pt')
            
            print("SAVED THE FBH GRADIENT INPUTS..")
        elif grad_input==None or grad_input[0]==None:
            print("GRADIENT INPUTS FBH CANNOT BE SAVED SINCE THEY ARE NULL...")
            
            
            
            
        if grad_output!=None and grad_output[0]!=None:
            save_batch_tensors_grad_output=grad_output[0]
            torch.save(save_batch_tensors_grad_output, f'{dir_name}/grad_output_{self.iteration_idx_fbh}_batch_size_{BATCH_SIZE}_layer_{self.layer_index}_full_backward_hook_tensor.pt')
            
            print("SAVED THE FBH GRADIENT OUTPUTS..")
        elif grad_output==None or grad_output[0]==None:
            print("GRADIENT OUTPUTS FBH CANNOT BE SAVED SINCE THEY ARE NULL...")
        self.iteration_idx_fbh+=1
        
        print()
        return grad_input
            
        
    def full_backward_hook_function(self,module,grad_input,grad_output):
        
        if grad_input[0]==None or grad_input==None:
            print("TO BE RETURNED VALUE IS NONE . CHANGES CANNOT BE DONE , RETURNING ......")
            return 
        
        
        grad_new_input=grad_input[0]
        
        
        
        if self.noise_input_fbh==None and self.new_values_input_fbh==None:
            print("NEITHER NOISE NOR NEW VALUES WERE PROVIDED FOR INPUTS TO BE UPGRADED FOR FBH , RETURNING OLD VALUES .....")
            return (grad_new_input,)
        
        
        if self.new_values_input_fbh==None:
            print("NEW VALUES NOT PROVIDED IN FBH SO UPDATING WITH OLD VALUES")

         
        elif self.new_values_input_fbh!=None:
            grad_new_input=self.new_values_input_fbh
            print("NEW VALUES PROVIDED IN FBH SO UPDATING WITH NEW VALUES")
        
        if self.noise_input_fbh==None:
            print("NOISE NOT PROVIDED IN FBH SO UPDATING WITH 1")
            return (grad_new_input,)
            
        elif self.noise_input_fbh!=None:
            print("NOISE PROVIDED IN FBH SO UPDATING ")
            return (grad_new_input*self.noise_input_fbh,)

        
            
     
    
        
    def register_fbh(self,update=False,visualize=False,add_noise_input=False,add_values_input=False,noise_input=None,new_values_input=None):
        if update==False and visualize==False:
            print("YOU CAN VISUALIZE OR UPDATE")
            return
        if update==True:
            if add_noise_input==True:
                self.noise_input_fbh=noise_input
            if add_values_input==True:
                self.new_values_input_fbh=new_values_input


            return self.layers[self.layer_index].register_full_backward_hook(self.full_backward_hook_function)
        elif visualize==True:
            return self.layers[self.layer_index].register_full_backward_hook(self.visualize_full_backward_hook_function)

        
        

        
        
        
        
        
        
        
        
        
        
        
        
        
    def visualize_full_backward_pre_hook_function(self,module,grad_output):
        print("VISUALIZING FBPH ITERATION INDEX : ",self.iteration_idx_fbph)
        BATCH_SIZE=grad_output[0].shape[0]
        dir_name="saved_full_backward_prehook_gradients"
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
            print(f"DIRECTORY {dir_name} CREATED.")
        else:
            print(f"DIRECTORY {dir_name} ALREADY EXISTS.")
        print("STARTING TO SAVE THE FBPH GRADIENTS")
        
        
        if grad_output!=None and grad_output[0]!=None:
            save_batch_tensors_grad_output=grad_output[0]

            torch.save(save_batch_tensors_grad_output, f'{dir_name}/grad_output_{self.iteration_idx_fbph}_batch_size_{BATCH_SIZE}_layer_{self.layer_index}_full_backward_prehook_tensor.pt')
            
            print("SAVED THE FBPH GRADIENT OUTPUTS...")
        elif grad_output==None or grad_output[0]==None:
            print("GRADIENT OUTPUTS FBPH CANNOT BE SAVED SINCE THEY ARE NULL...")
        self.iteration_idx_fbph+=1
        
        print()
        
        
       
        return grad_output
       
        
        
        
        
        
    def full_backward_pre_hook_function(self,module,grad_output):
        
        if grad_output==None or grad_output[0]==None:
            print("TO BE RETURNED VALUE IS NONE . CHANGES CANNOT BE DONE , RETURNING ......")
            return 
        grad_new=grad_output[0]
        
        if self.noise_output_fbph==None and self.new_values_output_fbph==None:
            print("NEITHER NOISE NOR NEW VALUES WERE PROVIDED FOR FBPH , RETURNING OLD VALUES .....")
            return (grad_new,)
        
        
        if self.new_values_output_fbph==None:
            print("NEW VALUES NOT PROVIDED IN FBPH SO UPDATING WITH OLD VALUES")

         
        elif self.new_values_output_fbph!=None:
            grad_new=self.new_values_output_fbph
            print("NEW VALUES PROVIDED IN FBPH SO UPDATING WITH NEW VALUES")
        
        if self.noise_output_fbph==None:
            print("NOISE NOT PROVIDED IN FBPH SO UPDATING WITH 1")
            return (grad_new,)
            
        elif self.noise_output_fbph!=None:
            print("NOISE PROVIDED IN FBPH SO UPDATING ")
            return (grad_new*self.noise_output_fbph,)

        
            
    
    
        
    
        
        
        
    def register_fbph(self,update=False,visualize=False,add_noise_output=False,add_values_output=False,noise_output=None,new_values_output=None):
        if update==False and visualize==False:
            print("YOU CAN VISUALIZE OR UPDATE")
            return
        if update==True:
            if add_noise_output==True:
                self.noise_output_fbph=noise_output
            if add_values_output==True:
                self.new_values_output_fbph=new_values_output
                
                    
                        
            return self.layers[self.layer_index].register_full_backward_pre_hook(self.full_backward_pre_hook_function)
        elif visualize==True:
            return self.layers[self.layer_index].register_full_backward_pre_hook(self.visualize_full_backward_pre_hook_function)
            
            
            
        
