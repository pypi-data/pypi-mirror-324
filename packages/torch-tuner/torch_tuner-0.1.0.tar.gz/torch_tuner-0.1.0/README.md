# **TorchTuner**

## Torch tuner is a pytorch package that lets the user to register the hooks for a specific layer in a PyTorch Neural Network . This library lets you register hooks naming : 

  * Forward Hook
  * Forward Pre-Hook
  * Full Backward-Hook
  * Full Backward Pre-Hook


#### Below are its applications after registering a hook :


### 1. Visualize :  It saves the respective parameters that are passed into the Hook Function of that layer , as a torch tensor . Folders are created in root directory to save them .

### 2. Update : It lets the user to update the respective parameters that are passed into the Hook Function of that layer . The updation is done in two ways by :

*    #### Noise : If noise is passed then it updates the values by factor of a noise and then returns the updated values
*    #### Values : Return the new values if they are simply passed . When both the noise and new values are passed it will first update the new values by a factor of noise and then returns them.



#### As of this version you can only attach the various hooks to only a single layer by a specific instance of this library . A register method returns a handle as returned by pytorch to rmove the specific registered hook . 



## USAGE

### VISUALIZE

#### Set the parameter "visualize" to ```True``` . It will automatically save the tensor .

### UPDATE

#### To update the values whether it gradient or simple value you must set the "update" parameter to ```True``` and pass the respective values while registering a hook .

#### To add the noise, just register the specific hook for that layer and use it. 

#### To update the values . Follow below steps :

* Get the shapes of that layer using the ```get_shape_of_layer``` . It returns ```input-shape``` and ```output-shape``` .
* Create the tensor of shape ```(BATCH_SIZE,respective_value)``` . This respective_value could be the ```input-shape``` or ```output-shape```  of that layer . This is determined by the output value the registered **```HOOK```** returns . If that hook returns the ```input``` values which are passed in the hook function then the ```respective_value``` will be the ```input-shape``` else if it returns ```output``` values then it will be the ```output-shape``` shape.