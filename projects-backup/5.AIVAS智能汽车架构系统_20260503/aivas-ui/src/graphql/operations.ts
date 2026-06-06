import { gql } from "@apollo/client";

export const GET_PROJECTS = gql`
  query GetProjects {
    projects {
      id
      name
      description
    }
  }
`;

export const GET_PROJECT = gql`
  query GetProject($id: ID!) {
    project(id: $id) {
      id
      name
      description
    }
  }
`;

export const CREATE_PROJECT = gql`
  mutation CreateProject($input: ProjectInput!) {
    createProject(input: $input) {
      id
      name
      description
    }
  }
`;

export const GET_TAGS = gql`
  query GetTags($projectId: ID!) {
    tags(projectId: $projectId) {
      id
      projectId
      level
      name
      description
      parentTagId
    }
  }
`;

export const CREATE_TAG = gql`
  mutation CreateTag($projectId: ID!, $input: TagInput!) {
    createTag(projectId: $projectId, input: $input) {
      id
      projectId
      level
      name
    }
  }
`;

export const GET_REQUIREMENTS = gql`
  query GetRequirements($projectId: ID!, $type: String) {
    requirements(projectId: $projectId, type: $type) {
      id
      projectId
      type
      content
      tagId
      version
      parentReqId
    }
  }
`;

export const CREATE_REQUIREMENT = gql`
  mutation CreateRequirement($projectId: ID!, $input: RequirementInput!) {
    createRequirement(projectId: $projectId, input: $input) {
      id
      projectId
      type
      content
    }
  }
`;

export const GET_DIAGRAM = gql`
  query GetDiagram($projectId: String!, $diagramType: String!) {
    diagram(projectId: $projectId, diagramType: $diagramType) {
      diagramType
      nodes {
        id
        type
        data_label
        data_description
        position_x
        position_y
      }
      edges {
        id
        source
        target
        animated
        label
      }
    }
  }
`;

export const SEND_MESSAGE = gql`
  mutation SendMessage($projectId: String!, $message: String!) {
    sendMessage(projectId: $projectId, message: $message) {
      answer
      sources
      diagram
    }
  }
`;

export const GET_RFLP_SUMMARY = gql`
  query GetRFLPSummary($projectId: String!) {
    rflpSummary(projectId: $projectId) {
      projectId
      requirements
      functions
      scs
      sscs
      ecus
      orphanFunctions
      orphanScs
    }
  }
`;
