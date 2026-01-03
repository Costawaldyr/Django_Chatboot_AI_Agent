from django.urls import path
from . import views
from .views import(
    AgentListView,
    AgentDetailView,
    AgentCreateView,
    AgentUpdateView,
    AgentDeleteView,
    UserAgentListView,
    UserProfileView,
    chat_view,
    send_message,
    get_messages,
)

urlpatterns = [
    path('', AgentListView.as_view(), name='home'),
    path('agent/new/', AgentCreateView.as_view(),name='agent-create'),
    path('agent/<uuid:pk>/', AgentDetailView.as_view(), name='agent-detail'),
    path('agent/<uuid:pk>/update/', AgentUpdateView.as_view(), name='agent-update'),
    path('agent/<uuid:pk>/delete/', AgentDeleteView.as_view(), name='agent-delete'),

    path('user/<str:username>/agents/', UserAgentListView.as_view(), name='user-agents'),
    path('user/<str:username>/profile/', UserProfileView.as_view(), name='user-profile'),

    path('agent/<uuid:pk>/chat/', chat_view, name='agent-chat'),
    path('agent/<uuid:pk>/chat/send/', send_message, name='send-message'),
    path("agent/<uuid:pk>/chat/messages/", get_messages, name="get-messages"),
    
    path('chat-b2/', views.chat_b2, name="chat-b2"),
    path('proxy/chat-txt/', views.proxy_chat_txt, name='proxy-chat-txt'),

    path('about/',views.about_view,name="about" ),
]
