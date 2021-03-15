from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from .models import Questao, Curso, Participante, Opcao, Mensagem
import datetime
from django.utils import timezone
from . import help

# function to get/Set the global variable help so it can be used in every function
def righta(r, num):
    if r:
        return help.ar
    else:
        help.ar = num

# Home page
def index(request):
    course_list = Curso.objects.all()[:5]
    template = loader.get_template('cursoOnline/index.html')
    context = {'course_list': course_list }
    return HttpResponse(template.render(context, request))

#Log In page
def logInSignIn(request, curso_id):
    curso = get_object_or_404(Curso, pk=curso_id)
    template = loader.get_template('cursoOnline/logInSignIn.html')
    context = {'curso': curso}
    if request.method == 'POST':
        if 'Login' in request.POST:
            # Gets the User if exists
            aux = Participante.objects.all().filter(nome=request.POST.get('nome')).filter(password=request.POST.get('senha')).values('id', 'curso')
            if aux:
                # Gets the course the user is afiliated to
                aux2 = Curso.objects.all().filter(id=(aux[0])['curso']).values('id')
                aaux2 =(int)((aux2[0])['id'])
                if aaux2 and aaux2 == (int)(curso_id):
                    aaux = (aux[0])['id']
                    participante_id = aaux
                    # Returns the Course Page
                    return HttpResponseRedirect(reverse('cursoOnline:cursoHub', args=(curso_id, participante_id)))
            else:
                # Returns the user to the login screen
                template = loader.get_template('cursoOnline/errorLogIn.html')
                context = {'curso': curso}
                return HttpResponse(template.render(context, request))
        else:
            # Returns the Sign up Page
            return HttpResponseRedirect(reverse('cursoOnline:form', args=curso_id))
    else:
        return HttpResponse(template.render(context, request))

# Sing Up page
def form(request, curso_id):
    # gets Course to Sign Up in
    curso = get_object_or_404(Curso, pk=curso_id)
    if request.method == 'POST':
        # Checks if the name password combo already exists
        aux = Participante.objects.all().filter(nome=request.POST.get('nome')).filter(password=request.POST.get('senha')).values('id')
        # Checks Name and Password Requirements (If Name has more than 3 charcters and password has more than 5
        if (request.POST.get('nome') and request.POST.get('senha')) and (len(request.POST.get('nome')) > 3 and len(request.POST.get('senha')) > 5):
            # If the user doesn't exist and the name and password pass the requirements adds the new user
            if not aux:
                p = Participante()
                p.nome = request.POST.get('nome')
                p.password = request.POST.get('senha')
                p.curso = Curso.objects.get(pk=curso_id)
                p.save()
                participante_id = ((Participante.objects.all().filter(nome=request.POST.get('nome')).filter(password=request.POST.get('senha')).values('id'))[0])['id']
            # If the user exists logs the user in
            else:
                aaux = (aux[0])['id']
                participante_id = aaux
            # Returns the courseHub page
            return HttpResponseRedirect(reverse('cursoOnline:cursoHub', args=(curso_id, participante_id)))
        # Returns th esing up page with  the sign up error "Name and/or Password have not met requirements"
        else:
            template = loader.get_template('cursoOnline/errorSignIn.html')
            context = {'curso': curso}
            return HttpResponse(template.render(context, request))
    # Returns the Sign Up page
    else:
        return render(request, 'cursoOnline/form.html', {'curso': curso})

#Course hub page
def cursoHub(request, curso_id, participante_id):
    # Gets User(Participante) and curso(Course)
    participante = get_object_or_404(Participante, pk=participante_id)
    curso = get_object_or_404(Curso, pk=curso_id)
    template = loader.get_template('cursoOnline/cursoHub.html')
    context = {'curso': curso, 'participante': participante}
    if request.method == 'POST':
        # Cheks Post method and redirects user to the chosen page
        if 'messageboard' in request.POST:
            # Returns Message Board Page
            return HttpResponseRedirect(reverse('cursoOnline:cursoChat', args=(curso_id, participante_id)))
        elif 'answerquestions' in request.POST:
            # Returns quiz page
            return HttpResponseRedirect(reverse('cursoOnline:cursoQuestoes', args=(curso_id, participante_id)))
        elif 'videos' in request.POST:
            # Returns Video playlists page
            return HttpResponseRedirect(reverse('cursoOnline:cursoVideos', args=(curso_id, participante_id)))
        else:
            # Returns finish course page
            return HttpResponseRedirect(reverse('cursoOnline:cursoFim', args=(curso_id, participante_id)))
    # Returns the course hub page
    else:
        return HttpResponse(template.render(context, request))

#Video Playlits Page
def cursoVideos(request, curso_id, participante_id):
    # Gets user(Participante) and course(Curso)
    participante = get_object_or_404(Participante, pk=participante_id)
    curso = get_object_or_404(Curso, pk=curso_id)
    template = loader.get_template('cursoOnline/cursoVideos.html')
    context = {'curso': curso, 'participante': participante}
    # Returns Video playlists page
    return HttpResponse(template.render(context, request))

#Quiz Page
def cursoQuestoes(request, curso_id, participante_id):
    # Gets user(Participante) and course(Curso) the question list associated to the course(question_list)
    participante = get_object_or_404(Participante, pk=participante_id)
    curso = get_object_or_404(Curso, pk=curso_id)
    question_list = Questao.objects.all().filter(curso=curso_id).order_by('?')[:5]
    template = loader.get_template('cursoOnline/cursoQuestoes.html')
    questions=Questao.objects.all()
    context = {'curso': curso, 'participante': participante, 'question_list': question_list}
    if request.method == 'POST':
        right = 0
        # Gets answers and checks if they are correct
        for q in questions:
            try:
                s = 'opcaoQ' + str(q.id)
                if request.POST.get(s):
                    opcao_selecionada = q.opcao_set.get(pk=request.POST.get(s))
                else:
                    continue
            except (KeyError, Opcao.DoesNotExist):
                # Returns an error if the user hasn't answered all the questions
                return render(request, 'cursoOnline/cursoQuestoes.html', {'q': q, 'error_message': "Não escolheu uma opção", })
            else:
                # Checks if the answer is correct and if so adds one to the correct question counter("right")
                if opcao_selecionada.certo:
                    right += 1
        righta(0, right)
        # Checks if user passed i.e. got 3 or more questions right
        if right >= 3:
            # Changes passed atribute to true wich means the user can now finish the course
            participante.passed = True
            participante.save()
            # Returns "right" page
            return HttpResponseRedirect(reverse('cursoOnline:right', args=(curso_id, participante_id)))
        else:
            # Returns "wrong" page
            return HttpResponseRedirect(reverse('cursoOnline:wrong', args=(curso_id, participante_id)))
    # Returns the quiz page
    else:
        return HttpResponse(template.render(context, request))

#Message Board page
def cursoChat(request, curso_id, participante_id):
    # Gets user(Participante) and course(Curso)
    participante = get_object_or_404(Participante, pk=participante_id)
    curso = get_object_or_404(Curso, pk=curso_id)
    template = loader.get_template('cursoOnline/cursoChat.html')
    # Filters by date
    today_min = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
    today_max = datetime.datetime.combine(datetime.date.today(), datetime.time.max)
    lWeek_min= today_min - datetime.timedelta(weeks=1)
    lMonth_min = today_min - datetime.timedelta(weeks=4)
    if request.method == 'POST':
        # Checks if the user wants to make a post
        if 'Post' in request.POST:
            m = Mensagem()
            # Checks if it is a regular post or a post with a media link
            if request.POST.get('islink') == 'on':
                m.isLink = True
                m.link = request.POST.get('link')
            m.content = request.POST.get('content')
            m.participante = Participante.objects.get(pk=participante_id)
            m.curso = Curso.objects.get(pk=curso_id)
            m.pub_date = timezone.now()
            m.save()
            # Returns message board page with the new post
            return HttpResponseRedirect(reverse('cursoOnline:cursoChat', args=(curso_id, participante_id)))
        # Checks if the user wants to upvote something
        elif 'm_idU' in request.POST:
            m = Mensagem.objects.get(pk=request.POST.get('m_idU'))
            m.upvotes = m.upvotes + 1
            m.save()
            # Returns the message board page with the updated upvotes
            return HttpResponseRedirect(reverse('cursoOnline:cursoChat', args=(curso_id, participante_id)))
        # Checks if the user wants to downvote something
        elif 'm_idD' in request.POST:
            m = Mensagem.objects.get(pk=request.POST.get('m_idD'))
            m.downvotes = m.downvotes + 1
            m.save()
            # Returns the message board page with the updated upvotes
            return HttpResponseRedirect(reverse('cursoOnline:cursoChat', args=(curso_id, participante_id)))
        # Checks if the user wants to sort the messages
        elif 'sort' in request.POST:
            # If the Filter is Today and Sort is MostRecent
            if request.POST.get('sort') == 'Most Recent' and request.POST.get('filtro') == 'Today':
                sort = request.POST.get('sort')
                filtro = request.POST.get('filtro')
                message_list = Mensagem.objects.all().filter(curso=curso_id).filter(pub_date__range=(today_min, today_max)).order_by('pub_date')
                context = {'curso': curso, 'participante': participante, 'message_list': message_list, 'sort' : sort, 'filtro' : filtro}
                #Returns the page filtered by "Today" and sorted by "Most Recent"
                return HttpResponse(template.render(context, request))
            # If the filter is "Last Week" and the sort is "Most Recent"
            elif request.POST.get('sort') == 'Most Recent' and request.POST.get('filtro') == 'Last Week':
                message_list = Mensagem.objects.all().filter(curso=curso_id).filter(pub_date__range=(lWeek_min, today_max)).order_by('pub_date')
                context = {'curso': curso, 'participante': participante, 'message_list': message_list}
                #Returns the page filtered by "Last Week" and sorted by "Most Recent"
                return HttpResponse(template.render(context, request))
            # If the filter is "Last Month" and the sort is "Most Recent"
            elif request.POST.get('sort') == 'Most Recent' and request.POST.get('filtro') == 'Last Month':
                message_list = Mensagem.objects.all().filter(curso=curso_id).filter(pub_date__range=(lMonth_min, today_max)).order_by('pub_date')
                context = {'curso': curso, 'participante': participante, 'message_list': message_list}
                #Returns the page filtered by "Last Month" and sorted by "Most Recent"
                return HttpResponse(template.render(context, request))
            # If the filter is "All Time" and the sort is "Most Recent"
            elif request.POST.get('sort') == 'Most Recent' and request.POST.get('filtro') == 'All Time':
                message_list = Mensagem.objects.all().filter(curso=curso_id).order_by('pub_date')
                context = {'curso': curso, 'participante': participante, 'message_list': message_list}
                # Returns the page filtered by "All Time" and sorted by "Most Recent"
                return HttpResponse(template.render(context, request))
            # If the filter is "Today" and the sort is "Upvotes"
            elif request.POST.get('sort') == 'Upvotes' and request.POST.get('filtro') == 'Today':
                message_list = Mensagem.objects.all().filter(curso=curso_id).filter(pub_date__range=(today_min, today_max)).order_by('-upvotes')
                context = {'curso': curso, 'participante': participante, 'message_list': message_list}
                # Returns the page filtered by "Today" and sorted by "Upvotes"
                return HttpResponse(template.render(context, request))
            # If the filter is "Last Week" and the sort is "Upvotes"
            elif request.POST.get('sort') == 'Upvotes' and request.POST.get('filtro') == 'Last Week':
                message_list = Mensagem.objects.all().filter(curso=curso_id).filter(pub_date__range=(lWeek_min, today_max)).order_by('-upvotes')
                context = {'curso': curso, 'participante': participante, 'message_list': message_list}
                # Returns the page filtered by "Last Week" and sorted by "Upvotes"
                return HttpResponse(template.render(context, request))
            # If the filter is "Last Month" and the sort is "Upvotes"
            elif request.POST.get('sort') == 'Upvotes' and request.POST.get('filtro') == 'Last Month':
                message_list = Mensagem.objects.all().filter(curso=curso_id).filter(pub_date__range=(lMonth_min, today_max)).order_by('-upvotes')
                context = {'curso': curso, 'participante': participante, 'message_list': message_list}
                # Returns the page filtered by "Last Month" and sorted by "Upvotes"
                return HttpResponse(template.render(context, request))
            # If the filter is "All Time" and the sort is "Upvotes"
            elif request.POST.get('sort') == 'Upvotes' and request.POST.get('filtro') == 'All Time':
                message_list = Mensagem.objects.all().filter(curso=curso_id).order_by('-upvotes')
                context = {'curso': curso, 'participante': participante, 'message_list': message_list}
                # Returns the page filtered by "All Time" and sorted by "Upvotes"
                return HttpResponse(template.render(context, request))
            # If the filter is "Today" and the sort is "Downvotes"
            elif request.POST.get('sort') == 'Downvotes' and request.POST.get('filtro') == 'Today':
                message_list = Mensagem.objects.all().filter(curso=curso_id).filter(pub_date__range=(today_min, today_max)).order_by('-downvotes')
                context = {'curso': curso, 'participante': participante, 'message_list': message_list}
                # Returns the page filtered by "Today" and sorted by "Downvotes"
                return HttpResponse(template.render(context, request))
            # If the filter is "Last Week" and the sort is "Downvotes"
            elif request.POST.get('sort') == 'Downvotes' and request.POST.get('filtro') == 'Last Week':
                message_list = Mensagem.objects.all().filter(curso=curso_id).filter(pub_date__range=(lWeek_min, today_max)).order_by('-downvotes')
                context = {'curso': curso, 'participante': participante, 'message_list': message_list}
                # Returns the page filtered by "Last Week" and sorted by "Downvotes"
                return HttpResponse(template.render(context, request))
            # If the filter is "Last Month" and the sort is "Downvotes"
            elif request.POST.get('sort') == 'Downvotes' and request.POST.get('filtro') == 'Last Month':
                message_list = Mensagem.objects.all().filter(curso=curso_id).filter(pub_date__range=(lMonth_min, today_max)).order_by('-downvotes')
                context = {'curso': curso, 'participante': participante, 'message_list': message_list}
                # Returns the page filtered by "Last Month" and sorted by "Downvotes"
                return HttpResponse(template.render(context, request))
            # If the filter is "All Time" and the sort is "Downvotes"
            elif request.POST.get('sort') == 'Downvotes' and request.POST.get('filtro') == 'All Time':
                message_list = Mensagem.objects.all().filter(curso=curso_id).order_by('downvotes')
                context = {'curso': curso, 'participante': participante, 'message_list': message_list}
                # Returns the page filtered by "All Time" and sorted by "Downvotes"
                return HttpResponse(template.render(context, request))
            # If the filter is "Today" and the sort is "UpDownvotes"
            elif request.POST.get('sort') == 'UpDownvotes' and request.POST.get('filtro') == 'Today':
                message_list = Mensagem.objects.all().filter(curso=curso_id).filter(pub_date__range=(today_min, today_max)).order_by('-upvotes', 'downvotes')
                context = {'curso': curso, 'participante': participante, 'message_list': message_list}
                # Returns the page filtered by "Today" and sorted by "UpDownvotes"
                return HttpResponse(template.render(context, request))
            # If the filter is "Last Week" and the sort is "UpDownvotes"
            elif request.POST.get('sort') == 'UpDownvotes' and request.POST.get('filtro') == 'Last Week':
                message_list = Mensagem.objects.all().filter(curso=curso_id).filter(pub_date__range=(lWeek_min, today_max)).order_by('-upvotes', 'downvotes')
                context = {'curso': curso, 'participante': participante, 'message_list': message_list}
                # Returns the page filtered by "Last Week" and sorted by "UpDownvotes"
                return HttpResponse(template.render(context, request))
            # If the filter is "Last Month" and the sort is "UpDownvotes"
            elif request.POST.get('sort') == 'UpDownvotes' and request.POST.get('filtro') == 'Last Month':
                message_list = Mensagem.objects.all().filter(curso=curso_id).filter(pub_date__range=(lMonth_min, today_max)).order_by('-upvotes', 'downvotes')
                context = {'curso': curso, 'participante': participante, 'message_list': message_list}
                # Returns the page filtered by "Last Month" and sorted by "UpDownvotes"
                return HttpResponse(template.render(context, request))
            # If the filter is "All Time" and the sort is "UpDownvotes"
            else:
                message_list = Mensagem.objects.all().filter(curso=curso_id).order_by('-upvotes', 'downvotes')
                context = {'curso': curso, 'participante': participante, 'message_list': message_list}
                # Returns the page filtered by "All Time" and sorted by "UpDownvotes"
                return HttpResponse(template.render(context, request))
    # Returns message board Page
    else:
        message_list = Mensagem.objects.all().filter(curso=curso_id).filter(pub_date__range=(today_min, today_max)).order_by('pub_date')
        context = {'curso': curso, 'participante': participante, 'message_list': message_list}
        return HttpResponse(template.render(context, request))

# Finish course page
def cursoFim(request, curso_id, participante_id):
    # Gets user(Participante) and course(Curso) and the course list excluding the current course the user is enrolled in (curso_list)
    participante = get_object_or_404(Participante, pk=participante_id)
    curso = get_object_or_404(Curso, pk=curso_id)
    template = loader.get_template('cursoOnline/cursoFim.html')
    curso_list = Curso.objects.all().exclude(id = curso_id)
    context = {'curso': curso, 'participante': participante, 'right': right, 'curso_list': curso_list}
    if request.method == 'POST':
        p = Participante.objects.get(pk=participante_id)
        # Checks if user wants to delete account or try a new course
        if 'endUser' in request.POST:
            #Deletes user
            Participante.objects.get(pk=participante_id).delete()
            #Returns Person to the Home page
            return HttpResponseRedirect(reverse('cursoOnline:index'))
        else:
            # Changes user's course and sets passed to False
            c=(Curso.objects.all().filter(nome=request.POST.get('curso')))[0]
            p.curso = c
            p.passed = False
            curso_id = c
            p.save()
            # Returns the hub page of the user's new course
            return HttpResponseRedirect(reverse('cursoOnline:cursoHub', args=(curso_id.id, participante_id)))
    # Returns Finish course page
    else:
        return HttpResponse(template.render(context, request))

#Right Page
def right(request, curso_id, participante_id):
    # Gets user(Participante) and course(Curso) and gets the amount of correct questions (right)
    right = righta(1, 0)
    participante = get_object_or_404(Participante, pk=participante_id)
    curso = get_object_or_404(Curso, pk=curso_id)
    template = loader.get_template('cursoOnline/right.html')
    context = {'curso': curso, 'participante': participante, 'right': right, 'curso_id': curso_id, 'participante_id': participante_id}
    # Returns right page with the number of correct answers
    return HttpResponse(template.render(context, request))

#Wrong Page
def wrong(request, curso_id, participante_id):
    # Gets user(Participante) and course(Curso) and gets the amount of correct questions (right)
    right = righta(1, 0)
    participante = get_object_or_404(Participante, pk=participante_id)
    curso = get_object_or_404(Curso, pk=curso_id)
    template = loader.get_template('cursoOnline/wrong.html')
    context = {'curso': curso, 'participante': participante, 'right': right}
    # Returns wrong page with the number of correct answers
    return HttpResponse(template.render(context, request))
