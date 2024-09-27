import numpy as np
import pylab,os
from matplotlib.widgets import Slider, RadioButtons, CheckButtons
import importlib

Kp = 0.1
Kd = 0.2
Ki = 0.0001
dt = 0.05
timelapse = 120
setpoint = 100
startpoint = 0
mass = 0.8
model = None
global saturation_on

class saturationMath:

    def __init__(self,max,min) -> None:
        self.max = max
        self.min = min

    def saturation(self,var):
        if var > self.max:
            return self.max
        elif var < self.min:
            return self.min
        else:
            return var

st = saturationMath(20,-5)

class PhysicModel:
    def __init__(self) -> None:
        pass

    def PhysModel(Kp, Kd, Ki, mass, dt, timelapse, setpoint, startpoint):
        t = 0
        currentpoint = startpoint
        currentspeed = 0
        old_error = 0
        sum = 0

        mov_by_points_list = [0]
        force_by_points_list = [0]

        while t < timelapse:
            t += dt
            error = setpoint - currentpoint
            force = Kp * error + Kd * ((error - old_error) / dt) + Ki * sum

            force = st.saturation(force)

            data = {'acc':9.81, 'mass':1}
            force -= model.model(**data)
            old_error = error
            sum += error

            acc = force / mass
            currentspeed += acc * dt
            currentpoint += currentspeed * dt + acc * pow(dt, 2) / 2

            mov_by_points_list.append(currentpoint)
            force_by_points_list.append(force * 2)

        return [mov_by_points_list, force_by_points_list]

class DravController:

    def frame():
        def update():
            output = PhysicModel.PhysModel(Kp.val, Kd.val, Ki.val, mass, dt, timelapse, setpoint, startpoint)
            movement = np.array(output[0])
            influence = np.array(output[1])
            time_scale = np.linspace(0, timelapse, int(timelapse / dt) + 2)

            graph_axes.clear()
            graph_axes.grid()
            graph_axes.set_ylim([-70, 200])
            graph_axes.plot(time_scale, movement, time_scale, influence)
            pylab.draw()


        def onChangeValue(value):
            update()

        fig, graph_axes = pylab.subplots()
        graph_axes.grid()
        fig.subplots_adjust(left=0.1, right=0.95, top=0.95, bottom=0.4)

        axes_slider_Kp = pylab.axes([0.05, 0.25, 0.85, 0.04])
        Kp = pylab.Slider(axes_slider_Kp, label='Kp',
                        valmin=0,
                        valmax=1.0,
                        valinit=0.28,
                        valfmt='%1.2f')

        axes_slider_Kd = pylab.axes([0.05, 0.18, 0.85, 0.04])
        Kd = pylab.Slider(axes_slider_Kd, label='Kd',
                        valmin=0,
                        valmax=1,
                        valinit=0.35,
                        valfmt='%1.2f')

        axes_slider_Ki = pylab.axes([0.05, 0.11, 0.85, 0.04])
        Ki = pylab.Slider(axes_slider_Ki, label='Ki',
                        valmin=0,
                        valmax=0.005,
                        valinit=0.002,
                        valfmt='%1.2f')

        Ki.on_changed(onChangeValue)
        Kd.on_changed(onChangeValue)
        Kp.on_changed(onChangeValue)

        update()
        pylab.show()


def decorator_function(getPlug):
    def wrapper():
        print("choose plugin")
        getPlug()
    return wrapper

@decorator_function
def getPlug():
    global model
    model = importlib.import_module("plug."+str(input()))


getPlug()

if __name__ == '__main__':
    
   DravController.frame()