from django.shortcuts import render,redirect,HttpResponse
from django.http import JsonResponse,HttpResponseRedirect
from .models import *
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
# import fitz 
# import spacy
# import random

# nlp = spacy.load("en_core_web_sm")

# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text()
            print("extracted text: ", text)
    return text

def extract_entities(text):
    doc = nlp(text)
    skills = []
    for ent in doc.ents:
        # Filter for relevant entities, e.g., skills, qualifications
        if ent.label_ in ("ORG", "PERSON", "GPE", "NORP", "SKILL", "WORK_OF_ART", "MISC",
                          "DATE", "TIME", "MONEY", "QUANTITY", "PERCENT", "LANGUAGE", 
                          "PRODUCT", "EVENT", "FAC", "DEGREE",):
            skills.append(ent.text.lower())
    return set(skills)
# Create your views here.

# def index(request):
#     return render(request, 'index.html')

def demo(request):
    return render(request, 'demo.html')

def jobseekindex(request):
    if 'jobseeker_id' in request.session:
        jobseeker_id=request.session['jobseeker_id']
        user=JobseekerRegister.objects.get(id=jobseeker_id)
        return render(request, 'jobseekindex.html', {'user':user})
    else:
        return redirect('jobseeker-login')
def jobprovideindex(request):
    if 'jobprovider_id' in request.session:
        jobprovide_id=request.session['jobprovider_id']
        user=JobproviderRegister.objects.get(id=jobprovide_id)
        return render(request, 'jobprovideindex.html', {'user':user})
    return redirect('jobproviderlogin')
def jobseekerreg(request):
    if request.method == 'POST':
        name=request.POST.get('name')
        email=request.POST.get('email')
        password=request.POST.get('password')
        number=request.POST.get('number')
        
        jobseek=JobseekerRegister(name=name, email=email, password=password, phone_number=number)
        jobseek.save()
        return redirect('jobseeker-login')
    return render(request, 'jobseekerreg.html')

def jobseekerlogin(request):
    if request.method == 'POST':
        email=request.POST.get('email')
        password=request.POST.get('password')
        try:
            jobseek=JobseekerRegister.objects.get(email=email, password=password)
            if jobseek:
                request.session['jobseeker_id'] = jobseek.id
                return redirect('jobseekerindex')
        except :
            alert="<script>alert('Invalid email or password'); window.location.href='/jobseeker-login/';</script>"
            return HttpResponse(alert)
    return render(request, 'jobseekerlogin.html')

def jobproviderreg(request):
    if request.method=='POST':
        name=request.POST.get('name')
        email=request.POST.get('email')
        password=request.POST.get('password')
        number=request.POST.get('number')
        cmpny_name=request.POST.get('company_name')
        
        jobprovider=JobproviderRegister(name=name, email=email, password=password, phone_number=number,company_name=cmpny_name)
        jobprovider.save()
        return redirect('jobproviderlogin')
    return render(request,'jobprovidereg.html')
    
def jobproviderlogin(request):
    if request.method=='POST':
        email=request.POST.get('email')
        password=request.POST.get('password')
        
        try:
            jobprovider=JobproviderRegister.objects.get(email=email, password=password)
            if jobprovider:
                request.session['jobprovider_id'] = jobprovider.id
                return redirect('jobprovideindex')
        except:
            alert="<script>alert('Invalid email or password'); window.location.href='/jobproviderlogin/';</script>"
            return HttpResponse(alert)
    return render(request, 'jobproviderlogin.html')


def jobseekprofile(request):
    if 'jobseeker_id' in request.session:
        jobseeker_id=request.session['jobseeker_id']
        user=JobseekerRegister.objects.get(id=jobseeker_id)
        msg = None
        msgi=None
        try:
            resumedtls=Resumes.objects.get(jobseeker=user)
            if resumedtls.resume_file is None:
                msg="no resume file"
            else:
                msgi=resumedtls
        except:
            msg = "No resume file uploaded."
            
        if request.method == "POST":
            resume_file = request.FILES.get('resume_file')
            resumes=Resumes(jobseeker=user, resume_file=resume_file)
            resumes.save()
            msg = "Resume uploaded successfully."
            return redirect('jobseekprofile')
            
        return render(request, 'jobseekprofile.html', {'user':user,'msg':msg,'msgi':msgi})
    else:
        return redirect('jobseeker-login')
    
def jobseekereditprofile(request):
    if 'jobseeker_id' in request.session:
        jobseeker_id=request.session['jobseeker_id']
        user=JobseekerRegister.objects.get(id=jobseeker_id)
        resumedtls=Resumes.objects.get(jobseeker=user)
        if request.method == 'POST':
            name=request.POST.get('name')
            email=request.POST.get('email')
            password=request.POST.get('password')
            number=request.POST.get('number')
            resum=request.FILES.get('resum')
            
            user.name=name
            user.email=email
            user.password=password
            user.phone_number=number
            if resum:
                resumedtls.resume_file=resum
            user.save()
            resumedtls.save()
            return redirect('jobseekprofile')
        return render(request, 'jobseekereditprofile.html', {'user':user, 'resumedtls':resumedtls})
    else:
        return redirect('jobseeker-login')
    
    
def jobproviderprofile(request):
    if 'jobprovider_id' in request.session:
        jobprovider_id = request.session['jobprovider_id']
        user = JobproviderRegister.objects.get(id=jobprovider_id)
        try:
            profile = JobProviderProfile.objects.get(jobprovider=user)
            return render(request, 'jobproviderprofile.html', {'user': user, 'profile': profile})
        except JobProviderProfile.DoesNotExist:
            if request.method == 'POST':
                company_logo = request.FILES.get('company_logo')
                description = request.POST.get('description')
                location = request.POST.get('location')
                profile = JobProviderProfile(jobprovider=user, company_logo=company_logo, company_description=description, address=location)
                profile.save()
                return redirect('jobproviderprofile')
            return render(request, 'jobproviderprofile.html', {'user': user, 'profile': None})

    else:
        return redirect('jobproviderlogin')
    
    
def jobprovidereditprofile(request):
    if 'jobprovider_id' in request.session:
        jobprovider_id = request.session['jobprovider_id']
        user = JobproviderRegister.objects.get(id=jobprovider_id)
        profile = JobProviderProfile.objects.get(jobprovider=user)
        if request.method == 'POST':
            company_logo = request.FILES.get('company_logo')
            description = request.POST.get('description')
            location = request.POST.get('location')
            
            user.name = request.POST.get('name')
            user.email = request.POST.get('email')
            user.password = request.POST.get('password')
            user.company_name = request.POST.get('company_name')
            
            if company_logo:
                profile.company_logo = company_logo
            profile.company_description = description
            
            profile.address = location
            
            user.save()
            profile.save()
            
            return redirect('jobproviderprofile')
        return render(request, 'jobprovidereditprofile.html', {'user': user, 'profile': profile})
    else:
        return redirect('jobproviderlogin')
    
    
def PostJob(request):
    if 'jobprovider_id' in request.session:
        jobprovider_id = request.session['jobprovider_id']
        user = JobproviderRegister.objects.get(id=jobprovider_id)
        if request.method == 'POST':
            title = request.POST.get('title')
            description = request.POST.get('description')
            
            job = Jobrequirements(jobprovider=user, job_title=title, job_description=description,status=True)
            job.save()
            
            return redirect('jobprovideindex')
        return render(request, 'postjob.html')
    else:
        return redirect('jobproviderlogin')
    
def viewJobs(request):
    if 'jobprovider_id' in request.session:
        jobprovider_id = request.session['jobprovider_id']
        user = JobproviderRegister.objects.get(id=jobprovider_id)
        jobs = Jobrequirements.objects.filter(jobprovider=user)
        return render(request, 'viewjobs.html', {'jobs': jobs})
    else:
        return redirect('jobproviderlogin')
    
def findJob(request):
    if 'jobseeker_id' in request.session:
        jobseeker_id = request.session['jobseeker_id']
        user = JobseekerRegister.objects.get(id=jobseeker_id)
        try:
            resumedtls = Resumes.objects.get(jobseeker=user)
        except :
            alert="<script>alert('no resume found!,please complete your profile );window.location.href='/jobseekprofile/';</script>"
            return HttpResponse(alert)
        jobs = Jobrequirements.objects.filter(status=True) 
        resume_path = resumedtls.resume_file.path
        resume_text = extract_text_from_pdf(resume_path)
        resume_entities = extract_entities(resume_text)
        print("R",resume_entities)

        matched_jobs = []
        for job in jobs:
            job_text = f"{job.job_title} {job.job_description}"
            job_entities = extract_entities(job_text)
            print(job_entities)
    
            if job_entities:
                matched_keywords = resume_entities.intersection(job_entities)
                # match_score = len(matched_keywords) / len(job_entities)
                match_score = len(resume_entities.intersection(job_entities)) / len(job_entities)
                print("Match score", match_score)
            else:
                match_score = 0  
                matched_keywords=set()

            if match_score > 0: 
                # matched_jobs.append((job, match_score))
                matched_jobs.append({
                    "job": job,
                    "score": match_score,
                    "matched_keywords": matched_keywords  
                })
        matched_jobs.sort(key=lambda x: x["score"], reverse=True)
        # matched_jobs.sort(key=lambda x: x[1], reverse=True)

        return render(request, 'findjobs.html', {'matched_jobs': matched_jobs})
    
    return redirect('jobseeker-login')


def apply_job(request,resid):
    if 'jobseeker_id' in request.session:
        jobseeker_id = request.session['jobseeker_id']
        user = JobseekerRegister.objects.get(id=jobseeker_id)
        job = Jobrequirements.objects.get(id=resid)
        jobprovid=job.jobprovider
        applied_jobs = JobApplications.objects.filter(jobseeker=user, job_requirements=job)
        if applied_jobs:
            alert="<script>alert('Already applied this job'); window.location.href='/findJob/';</script>"
            return HttpResponse(alert)
        
        applied_job = JobApplications(jobseeker=user, job_requirements=job,jobprovider=jobprovid,selected_status=False)
        applied_job.save()
        
        return redirect('jobseekerindex')
    return redirect('jobseeker-login')

def viewappiledjobsprovider(request):
    if 'jobprovider_id' in request.session:
        jobprovider_id = request.session['jobprovider_id']
        jobs = JobApplications.objects.filter(jobprovider__id=jobprovider_id).select_related('jobseeker', 'job_requirements')
        return render(request, 'viewappiledjobsprovider.html', {'jobs': jobs})
    return redirect('jobproviderlogin')
def toggle_status(request, application_id):
    if 'jobprovider_id' in request.session:
        application = JobApplications.objects.get(id=application_id)
        application.selected_status = not application.selected_status
        application.save()
    return redirect('viewapplication') 

def jobseekApplications(request):
    if 'jobseeker_id' in request.session:
        jobseeker_id = request.session['jobseeker_id']
        applications = JobApplications.objects.filter(jobseeker__id=jobseeker_id)
        return render(request, 'jobseekapplications.html', {'applications': applications})
    return redirect('jobseeker-login')
    
    
def EditjobReq(request, jobid):
    if 'jobprovider_id' in request.session:
        jobprovider_id = request.session['jobprovider_id']
        user = JobproviderRegister.objects.get(id=jobprovider_id)
        job = Jobrequirements.objects.get(id=jobid)
        if request.method == 'POST':
            title = request.POST.get('title')
            description = request.POST.get('description')
            status=request.POST.get('status')
            
            job.job_title = title
            job.job_description = description
            job.status = status
            
            job.save()
            
            return redirect('viewjobs')
        return render(request, 'editjobreq.html', {'job': job})
    return redirect('jobproviderlogin')

def Deletejob(request, jobid):
    if 'jobprovider_id' in request.session:
        job = Jobrequirements.objects.get(id=jobid)
        job.delete()
        return redirect('viewjobs')
    return redirect('jobproviderlogin')

def create_exam_and_questions(request):
    if 'jobprovider_id' in request.session:
        jobprovider_id = request.session['jobprovider_id']
        
        user = JobproviderRegister.objects.get(id=jobprovider_id)
        jobs = Jobrequirements.objects.get(jobprovider=user)
        if request.method == 'POST':
            title = request.POST.get('title')
            time_limit = request.POST.get('time_limit')
            questions = request.POST.getlist('questions')  
            max_marks_list = request.POST.getlist('max_marks')  
            
            exam = Exam(
                jobprovider=user,
                job_requirements=jobs,
                title=title,
                time_limit=time_limit
            )
            exam.save()

            for question_text, max_marks in zip(questions, max_marks_list):
                if question_text and max_marks.isdigit(): 
                    ExamQuestion.objects.create(
                        exam=exam,
                        question_text=question_text,
                        max_marks=int(max_marks)
                    )

            return redirect('viewapplication')

        return render(request, 'create_exam_and_questions.html')
    
    return redirect('jobproviderlogin')

def list_exams(request):
    if 'jobprovider_id' in request.session:
        jobprovider_id = request.session['jobprovider_id']
        
        # Retrieve all exams for the job provider
        exams = Exam.objects.filter(jobprovider_id=jobprovider_id)
        
        return render(request, 'list_exams.html', {'exams': exams})
    

    
    return redirect('jobproviderlogin')

def view_exam_questions(request, exam_id):
    if 'jobprovider_id' in request.session:
        jobprovider_id = request.session['jobprovider_id']
        exam = Exam.objects.get(id=exam_id, jobprovider_id=jobprovider_id)
        questions = exam.questions.all()  # Access related questions

        return render(request, 'view_exam_questions.html', {'exam': exam, 'questions': questions})

    return redirect('jobproviderlogin')


def generate_random_token(length=8):
    return ''.join(random.choices('0123456789', k=length))

def take_exam(request, exam_id):
    if 'jobseeker_id' in request.session:
        jobseeker_id = request.session['jobseeker_id']
        print(jobseeker_id)
        jobseeker = JobseekerRegister.objects.get(id=jobseeker_id)
        if not request.session.get('exam_token'):
            request.session['exam_token'] = generate_random_token()
    
        exam = get_object_or_404(Exam, id=exam_id)
        jobseeker = get_object_or_404(JobseekerRegister, id=jobseeker_id)
        
        if Answers.objects.filter(
                jobseeker=jobseeker,
                exam_question__exam=exam,
                exam_status=True
            ).exists():
            alert = "<script>alert('You have already attended this exam.'); window.location.replace('/jonseekindex/');</script>"
            return HttpResponse(alert)
    
        # Verify access via token
        if 'token' in request.GET and request.GET['token'] != request.session['exam_token']:
            return HttpResponse("Invalid access attempt.", status=403)
    
        if request.method == 'POST':
            responses = request.POST.getlist('responses')
            question_ids = request.POST.getlist('question_ids')
            warning_count = int(request.POST.get('warning_count', 0))

            for question_id, response in zip(question_ids, responses):
                question = get_object_or_404(ExamQuestion, id=question_id)
            
                # Get or create the answer instance for each question
                answer, created = Answers.objects.get_or_create(
                    jobseeker=jobseeker,
                    exam_question=question,
                    defaults={'answer': response}
                )
            
                # Update the answer if it already exists
                answer.answer = response

                # Log malpractice in the answer if any warnings were recorded
                if warning_count > 0:
                    answer.exam_log = (answer.exam_log or '') + f"\nMalpractice detected: {warning_count} warning(s)."
                    answer.exam_status = True
                else:
                    answer.exam_status = True
                    answer.exam_log ="no malpractise detected"
            
                answer.save()

            # Redirect all users to exam_completed regardless of malpractice status
            return JsonResponse({'redirect_url': redirect('exam_completed').url})

        # Display exam questions
        questions = exam.questions.all()
        return render(request, 'take_exam.html', {'exam': exam, 'questions': questions, 'jobseeker': jobseeker})
    return redirect('jobseeker-login')


from django.core.mail import send_mail
from django.urls import reverse
import secrets
from django.conf import settings
def send_exam_links_page(request):
    if 'jobprovider_id' in request.session:
        jobprovider_id = request.session['jobprovider_id']
        
        # Fetch all applications and exams related to the job provider
        applications = JobApplications.objects.filter(jobprovider_id=jobprovider_id).select_related('job_requirements', 'jobseeker')
        exams = Exam.objects.filter(jobprovider_id=jobprovider_id)
        
        context = {
            'applications': applications,
            'exams': exams,
        }
        
        return render(request, 'send_exam_links.html', context)
    return redirect('jobprovidelogin')


from django.contrib import messages
from django.core.exceptions import MultipleObjectsReturned
def send_exam_email(request, job_id, jobseeker_id):
    jobseeker = get_object_or_404(JobseekerRegister, id=jobseeker_id)
    exam_id = request.GET.get('exam_id')
    exam = get_object_or_404(Exam, id=exam_id)

    # Generate exam link
    exam_link = request.build_absolute_uri(reverse('take_exam', args=[exam.id]))

    try:
        send_mail(
            subject="Your Exam Link",
            message=(
                f"Hello {jobseeker.name},\n\n"
                "Please ensure you are logged in to the website before clicking this link; otherwise, you will be unable to access the exam.\n\n"
                f"Here is your exam link: {exam_link}\n\n"
                "Good luck!"
            ),
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[jobseeker.email],
            fail_silently=False,
        )
        messages.success(request, f"Exam link sent successfully to {jobseeker.email}.")
    except Exception as e:
        messages.error(request, f"Failed to send exam link to {jobseeker.email}. Error: {e}")

    return redirect('send_exam_links_page')


def exam_results(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)
    answers = Answers.objects.filter(exam_question__exam=exam, exam_status=True)

    if request.method == "POST":
        # Process form submission for adding/editing marks
        for answer in answers:
            marks_field = f'marks_{answer.id}'
            new_marks = request.POST.get(marks_field)
            if new_marks is not None:
                answer.marks_scored = int(new_marks)
                answer.save()
                return redirect('list_exams')
        return HttpResponseRedirect(reverse('exam_results', args=[exam_id]))

    return render(request, 'exam_results.html', {'exam': exam, 'answers': answers})

def DeleteExam(request, exmid):
    if 'jobprovider_id' in request.session:
        job = Exam.objects.get(id=exmid)
        job.delete()
        return redirect('list_exams')
    return redirect('jobproviderlogin')

def exam_completed(request):
    return render(request, 'exam_completed.html')

def exam_terminated(request):
    return HttpResponse('Exam terminated due to malpractice')
def logout(request):
    if 'jobprovider_id' in request.session:
        del request.session['jobprovider_id']
        return redirect('jobproviderlogin')
    elif 'jobseeker_id' in request.session:
        del request.session['jobseeker_id']
        return redirect('jobseeker-login')
    
  
  
  
def adminindex(request):
    if 'ademail' in request.session:
        jobsek = JobseekerRegister.objects.all()  # Get all job seekers
        jobpro = JobProviderProfile.objects.all()  # Get all job providers
        return render(request, 'adminindex.html', {'jobsek': jobsek, 'jobpro': jobpro})
    else:
        alert = "<script>alert('Please login as admin'); window.location.href='/admin_login/';</script>"
        return HttpResponse(alert)
def admin_log(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        if email == 'admin@gmail.com' and password == 'admin':
            request.session['ademail'] = email
            return redirect('admin_panel')
        else:
            alert="<script>alert('Invalid email or password'); window.location.href='/admin_log/';</script>"
            return HttpResponse(alert)
    return render(request, 'admin_login.html')


def admin_jobseekers(request):
    if 'ademail' not in request.session:
        alert = "<script>alert('Please login as admin'); window.location.href='/admin_log/';</script>"
        return HttpResponse(alert)

    jobseekers = JobseekerRegister.objects.all()
    return render(request, 'admin_jobseekers.html', {'jobseekers': jobseekers})

def edit_jobseeker(request, pk):
    jobseeker = get_object_or_404(JobseekerRegister, pk=pk)
    if request.method == 'POST':
        jobseeker.name = request.POST.get('name')
        jobseeker.email = request.POST.get('email')
        jobseeker.phone_number = request.POST.get('phone_number')
        jobseeker.save()
        messages.success(request, 'Job seeker updated successfully!')
        return redirect('admin_jobseekers')
    return render(request, 'edit_jobseeker.html', {'jobseeker': jobseeker})

def delete_jobseeker(request, pk):
    jobseeker = get_object_or_404(JobseekerRegister, pk=pk)
    jobseeker.delete()
    messages.success(request, 'Job seeker deleted successfully!')
    return redirect('admin_jobseekers')


def admin_jobproviders(request):
    if 'ademail' not in request.session:
        alert = "<script>alert('Please login as admin'); window.location.href='/admin_log/';</script>"
        return HttpResponse(alert)

    jobproviders = JobproviderRegister.objects.all()
    return render(request, 'admin_jobproviders.html', {'jobproviders': jobproviders})

def edit_jobprovider(request, pk):
    jobprovider = get_object_or_404(JobproviderRegister, pk=pk)
    profile = JobProviderProfile.objects.filter(jobprovider=jobprovider).first()

    if request.method == 'POST':
        jobprovider.name = request.POST.get('name')
        jobprovider.email = request.POST.get('email')
        jobprovider.phone_number = request.POST.get('phone_number')
        jobprovider.company_name = request.POST.get('company_name')
        jobprovider.save()

        # Update or create profile
        if profile:
            profile.company_description = request.POST.get('company_description')
            profile.address = request.POST.get('address')
            if request.FILES.get('company_logo'):
                profile.company_logo = request.FILES.get('company_logo')
            profile.save()
        else:
            # Create a new profile if it does not exist
            profile = JobProviderProfile(
                jobprovider=jobprovider,
                company_description=request.POST.get('company_description'),
                address=request.POST.get('address'),
                company_logo=request.FILES.get('company_logo')
            )
            profile.save()

        messages.success(request, 'Job provider and profile updated successfully!')
        return redirect('admin_jobproviders')

    return render(request, 'edit_jobprovider.html', {'jobprovider': jobprovider, 'profile': profile})

def delete_jobprovider(request, pk):
    jobprovider = get_object_or_404(JobproviderRegister, pk=pk)
    jobprovider.delete()
    messages.success(request, 'Job provider deleted successfully!')
    return redirect('admin_jobproviders')


def adlogout(request):
    if 'ademail' in request.session:
        del request.session['ademail']
        return redirect('admin_log')
    else:
        alert = "<script>alert('Please login as admin'); window.location.href='/admin_log/';</script>"
        return HttpResponse(alert)
    
        
        
    


        
        
        