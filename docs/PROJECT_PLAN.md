# Plan de Proyecto - Mejora de API REST con Patrones de Diseño

## 1. EQUIPO Y ROLES

### Roles Sugeridos (adaptables según equipo):
- **Product Owner / Líder de Proyecto**: Define requisitos y prioridades
- **Arquitecto de Software**: Diseña la arquitectura y selecciona patrones de diseño
- **Desarrollador Backend**: Implementa la lógica de negocio y refactorización
- **Tester / QA**: Crea y ejecuta pruebas unitarias e integración
- **Documentador**: Genera documentación técnica y diagramas UML

## 2. METODOLOGÍA ÁGILE: SCRUM

### ¿Por qué Scrum?
- Sprints cortos para iteraciones rápidas
- Revisiones frecuentes del código
- Adaptable a equipos pequeños (2-4 personas)

### Configuración del Sprint:
- **Duración del Sprint**: 1-2 semanas
- **Daily Standup**: 15 minutos (¿Qué hice? ¿Qué haré? ¿Bloqueadores?)
- **Sprint Review**: Demostración de funcionalidades completadas
- **Sprint Retrospective**: Mejora continua del proceso

### User Stories Principales:
1. **US-001**: Como desarrollador, quiero refactorizar el código para aplicar principios SOLID
2. **US-002**: Como arquitecto, quiero implementar patrones de diseño para mejorar la mantenibilidad
3. **US-003**: Como usuario, quiero recibir notificaciones cuando se agreguen productos a favoritos
4. **US-004**: Como tester, quiero pruebas automatizadas para garantizar calidad
5. **US-005**: Como desarrollador, quiero documentación clara de la arquitectura

## 3. ROADMAP DEL PROYECTO

### Sprint 1: Análisis y Refactorización Base
**Duración**: Semana 1

#### Tareas:
- [ ] Análisis del código existente
- [ ] Identificación de code smells y anti-patrones
- [ ] Creación de estructura de carpetas mejorada
- [ ] Implementación de patrón Repository
- [ ] Implementación de patrón Singleton para DB
- [ ] Refactorización de autenticación con Decorator Pattern

**Entregables**:
- Código refactorizado con separación de capas
- Diagrama de arquitectura inicial

### Sprint 2: Nuevo Módulo de Notificaciones
**Duración**: Semana 2

#### Tareas:
- [ ] Diseño del sistema de notificaciones
- [ ] Implementación de patrón Observer
- [ ] Implementación de patrón Strategy (Email, SMS, Push)
- [ ] Integración con módulo de favoritos
- [ ] Configuración de notificaciones

**Entregables**:
- Módulo de notificaciones funcional
- Diagramas UML del módulo

### Sprint 3: Testing y Documentación
**Duración**: Semana 3

#### Tareas:
- [ ] Pruebas unitarias (pytest)
- [ ] Pruebas de integración
- [ ] Documentación técnica completa
- [ ] Diagramas UML de clases y secuencia
- [ ] README actualizado

**Entregables**:
- Suite de pruebas completa
- Documentación técnica exhaustiva

## 4. ESTRATEGIA DE TESTING

### Niveles de Testing:

#### 4.1 Pruebas Unitarias
**Framework**: pytest
**Cobertura mínima**: 80%

**Componentes a testear**:
- Repositories (acceso a datos)
- Services (lógica de negocio)
- Validators (validación de datos)
- Notificación strategies

**Ejemplo**:
```python
def test_product_repository_get_all():
    repo = ProductRepository()
    products = repo.get_all()
    assert len(products) > 0
```

#### 4.2 Pruebas de Integración
**Framework**: pytest + Flask test client

**Escenarios**:
- Flujo completo de autenticación
- CRUD de productos con persistencia
- Sistema de notificaciones end-to-end

**Ejemplo**:
```python
def test_add_favorite_sends_notification():
    client = app.test_client()
    response = client.post('/favorites',
        json={'user_id': 1, 'product_id': 1},
        headers={'Authorization': 'valid_token'})
    assert response.status_code == 201
    # Verificar que se envió notificación
```

#### 4.3 Pruebas de API
**Herramienta**: Postman/Insomnia Collections

**Test cases**:
- Validación de respuestas HTTP
- Validación de estructura JSON
- Manejo de errores (401, 404, 400)

### Estrategia de CI/CD (Opcional):
- GitHub Actions para ejecutar tests automáticamente
- Pre-commit hooks para linting
- Coverage reports

## 5. PATRONES DE DISEÑO A IMPLEMENTAR

### 5.1 Patrones Creacionales
- **Singleton**: Gestión de conexión a base de datos
- **Factory**: Creación de estrategias de notificación

### 5.2 Patrones Estructurales
- **Repository**: Abstracción del acceso a datos
- **Decorator**: Middleware de autenticación
- **Adapter**: Adaptación de diferentes fuentes de datos

### 5.3 Patrones de Comportamiento
- **Strategy**: Diferentes tipos de notificaciones
- **Observer**: Sistema de eventos para notificaciones
- **Template Method**: Procesamiento de requests

## 6. DEFINICIÓN DE "DONE"

Una tarea está completada cuando:
- ✅ Código implementado y funcional
- ✅ Pruebas unitarias escritas y pasando
- ✅ Código revisado por al menos un compañero
- ✅ Documentación actualizada
- ✅ Sin errores de linting
- ✅ Commit con mensaje descriptivo

## 7. MÉTRICAS DE ÉXITO

- **Cobertura de código**: ≥ 80%
- **Complejidad ciclomática**: ≤ 10 por función
- **Duplicación de código**: ≤ 3%
- **Deuda técnica**: Reducción del 50%

## 8. RIESGOS Y MITIGACIÓN

| Riesgo | Probabilidad | Impacto | Mitigación |
|--------|--------------|---------|------------|
| Refactorización rompe funcionalidad | Media | Alto | Pruebas de regresión exhaustivas |
| Tiempo insuficiente | Alta | Medio | Priorización de features críticos |
| Falta de experiencia en patrones | Media | Medio | Pair programming y documentación |

## 9. HERRAMIENTAS Y TECNOLOGÍAS

- **Backend**: Flask, Flask-RESTful
- **Testing**: pytest, unittest, coverage
- **Linting**: pylint, flake8, black
- **Documentación**: Markdown, PlantUML, Sphinx
- **Control de versiones**: Git, GitHub
- **Gestión de proyecto**: GitHub Projects, Trello

## 10. SIGUIENTE PASOS

1. Revisar y aprobar este plan con el equipo
2. Asignar roles a cada miembro
3. Configurar entorno de desarrollo
4. Iniciar Sprint 1
