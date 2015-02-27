#ifndef GAEWINDOW_H
#define GAEWINDOW_H

#include <QMainWindow>

namespace Ui {
class GaeWindow;
}

class GaeWindow : public QMainWindow
{
        Q_OBJECT

    public:
        explicit GaeWindow(QWidget *parent = 0);
        ~GaeWindow();

    private:
        Ui::GaeWindow *ui;
};

#endif // GAEWINDOW_H
