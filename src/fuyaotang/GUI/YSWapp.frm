VERSION 5.00
Object = "{831FDD16-0C5C-11D2-A9FC-0000F8754DA1}#2.2#0"; "MSCOMCTL.OCX"
Begin VB.Form YSWapp 
   Caption         =   "fuyaotang.com数据读取系统"
   ClientHeight    =   7275
   ClientLeft      =   120
   ClientTop       =   465
   ClientWidth     =   11880
   LinkTopic       =   "Form1"
   ScaleHeight     =   7275
   ScaleWidth      =   11880
   StartUpPosition =   3  '窗口缺省
   Begin VB.Frame ChromeControlFrame 
      Caption         =   "模拟器设置"
      Height          =   6015
      Left            =   9000
      TabIndex        =   1
      Top             =   600
      Width           =   2775
      Begin VB.CommandButton InitialChromeBtn 
         Caption         =   "初始化浏览器"
         Height          =   495
         Left            =   480
         TabIndex        =   2
         Top             =   480
         Width           =   1695
      End
   End
   Begin VB.Frame MainFrame 
      Caption         =   "操作中心"
      Height          =   6015
      Left            =   120
      TabIndex        =   0
      Top             =   600
      Width           =   8775
      Begin MSComctlLib.ProgressBar ProgressBar1 
         Height          =   375
         Left            =   3960
         TabIndex        =   6
         Top             =   5400
         Width           =   4335
         _ExtentX        =   7646
         _ExtentY        =   661
         _Version        =   393216
         Appearance      =   1
      End
      Begin VB.CommandButton DoReadBtn 
         Caption         =   "下载选择的省市药店数据/下载所有"
         Height          =   615
         Left            =   4320
         TabIndex        =   5
         Top             =   1440
         Width           =   3735
      End
      Begin VB.CommandButton ReadListBtn 
         Caption         =   "读取省市列表"
         Height          =   615
         Left            =   4320
         TabIndex        =   4
         Top             =   480
         Width           =   3735
      End
      Begin VB.ListBox ProvinceCityListBox 
         Height          =   5460
         Left            =   240
         MultiSelect     =   2  'Extended
         TabIndex        =   3
         Top             =   360
         Width           =   3255
      End
   End
End
Attribute VB_Name = "YSWapp"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = False
