#include "GaeWindow.h"
#include "ui_GaeWindow.h"

GaeWindow::GaeWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::GaeWindow)
{
    ui->setupUi(this);
}

GaeWindow::~GaeWindow()
{
    delete ui;
}
