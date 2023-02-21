import fpdf
import line

class PATH:
    def __init__(self, pdf):
        self.path = pdf.new_path()

    def __enter__(self):
        path = self.path.__enter__()
        path.style.fill_color = None
        path.style.stroke_width = 0.1
        return path

    def __exit__(self, exc_type, exc_value, traceback):
        self.path.__exit__(exc_type, exc_value, traceback)

def draw(what):
    with PATH(what) as path:
        path.move_to(1, 1)
        path.line_to(2, 2)
        path.line_to(1, 2)
        path.close()

def draw(what):
    lines = line.run()
    for l in lines:
        with PATH(what) as path:
            x0,y0 = l[0]
            path.move_to(x0, y0)
            for j in range(len(l)-1):
                x1,y1 = l[j+1]
                path.line_to(x1,y1)
            path.close()

def run():
    pdf = fpdf.FPDF(unit='in', format=(10, 10))
    pdf.add_page()
    draw(pdf)
    pdf.output("test.pdf")

if __name__ == "__main__":
    run()
