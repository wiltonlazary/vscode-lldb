import io
import lldb
import adapter
import numpy as np
import matplotlib
matplotlib.use('svg')
import matplotlib.pyplot as plt

def show():
    image_svg = io.BytesIO()
    plt.savefig(image_svg, format='svg')
    adapter.preview_html('debugger:/foobar', title='Pretty Plot', position=2,
                         content={'debugger:/foobar': image_svg.getvalue()})

def showy():
    image_svg = io.BytesIO()
    plt.savefig(image_svg, format='svg')
    adapter.preview_html('debugger:/foo', title='Pretty Plot', position=2,
                         content={'debugger:/foo': '<html><body><script src="debugger:/bar/xxx"></script></body></html>',
                                  'debugger:/bar/xxx': image_svg.getvalue() })

def plot():
    x = np.linspace(0, 2 * np.pi, 500)
    y1 = np.sin(x)
    y2 = np.sin(3 * x)
    fig, ax = plt.subplots()
    ax.fill(x, y1, 'b', x, y2, 'r', alpha=0.3)
    show()

def plot_image(cmap='nipy_spectral_r'):
    xdim = lldb.frame.EvaluateExpression('xdim').GetValueAsSigned()
    ydim = lldb.frame.EvaluateExpression('ydim').GetValueAsSigned()
    image = lldb.frame.EvaluateExpression('image')
    data = lldb.process.ReadMemory(image.GetLoadAddress(), xdim * ydim * 4, lldb.SBError())
    data = np.frombuffer(data, dtype=np.int32).reshape((ydim,xdim))
    plt.imshow(data, cmap=cmap, interpolation='nearest')
    show()
