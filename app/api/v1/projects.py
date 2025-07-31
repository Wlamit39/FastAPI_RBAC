from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.db.database import get_session
from app.db.models import Project
from app.api.deps import get_current_user, require_admin
from app.schemas.project import ProjectCreate, ProjectUpdate, ProjectResponse
from typing import List
from app.db.models import User

router = APIRouter(prefix="/projects", tags=["Projects"])


@router.get("/", response_model=List[ProjectResponse])
def get_projects(session: Session = Depends(get_session), user: User = Depends(get_current_user)):
    return session.exec(select(Project)).all()


@router.post("/", response_model=ProjectResponse)
def create_project(data: ProjectCreate, session: Session = Depends(get_session), user: User = Depends(require_admin)):
    new_project = Project(name=data.name, description=data.description, owner_id=user.id)
    session.add(new_project)
    session.commit()
    session.refresh(new_project)
    return new_project


@router.put("/{project_id}", response_model=ProjectResponse)
def update_project(project_id: int, data: ProjectUpdate, session: Session = Depends(get_session), user: User = Depends(require_admin)):
    project = session.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    project.name = data.name
    project.description = data.description
    session.add(project)
    session.commit()
    session.refresh(project)
    return project


@router.delete("/{project_id}")
def delete_project(project_id: int, session: Session = Depends(get_session), user: User = Depends(require_admin)):
    project = session.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    session.delete(project)
    session.commit()
    return {"message": "Project deleted successfully"}
