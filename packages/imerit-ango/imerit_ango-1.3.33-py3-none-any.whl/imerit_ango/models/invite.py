from typing import List

from imerit_ango.models.enums import ProjectRoles, OrganizationRoles


class Invitation:
    def __init__(self, to: List[str], organization_role: OrganizationRoles, project_id: str = None, project_role: ProjectRoles = None):
        self.to = to
        self.organization_role = organization_role
        self.project_id = project_id
        self.project_role = project_role

    def toDict(self):
        resp = {
            'to': self.to,
            'organizationRole': self.organization_role.value,
            'projectId': self.project_id,
            'projectRole': self.project_role
        }
        if self.project_role:
            resp['projectRole'] = self.project_role.value
        return resp


class RoleUpdate:
    def __init__(self, email: str, organization_role: OrganizationRoles):
        self.email = email
        self.organization_role = organization_role

    def toDict(self):
        return {
            'email': self.email,
            'organizationRole': self.organization_role.value
        }

class ProjectMember:
    def __init__(self, email: str, project_role: ProjectRoles):
        self.email = email
        self.project_roles = project_role

    def toDict(self):
        return {
            'to': self.email,
            'projectRole': self.project_role.value
        }