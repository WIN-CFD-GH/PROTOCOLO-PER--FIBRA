
        // --- DATA STRUCTURE (Extracted from PDF Protocolo Perú Fibra 28.08.2026) ---
        // Organizado según el Índice solicitado para no omitir información.
        function switchGestionesTab(tabId, btnElement) {
        // Hide all tabs
        var tabs = document.querySelectorAll('#gestiones-tabs-container ~ div > .tab-content');
        tabs.forEach(function(tab) { return  {
            tab.classList.remove('block' });
            tab.classList.add('hidden');
        });
        
        // Remove active class from all buttons
        var btns = document.querySelectorAll('#gestiones-tabs-container .tab-btn');
        btns.forEach(function(btn) { return  {
            btn.classList.remove('active' });
        });
        
        // Show target tab
        document.getElementById(tabId).classList.remove('hidden');
        document.getElementById(tabId).classList.add('block');
        
        // Add active class to clicked button
        btnElement.classList.add('active');
    }

var protocolData = [
            {
                section: "1. NUESTROS LINEAMIENTOS",
                icon: "ph-star",
                cards: [
                    { title: "Transmite una actitud positiva", content: "Mantén una sonrisa telefónica." },
                    { title: "Personaliza tu atención", content: "<strong>VOZ INFORMAL:</strong> Si el cliente te llama por tu nombre, trátalo de tú y por su nombre.<br><strong>VOZ FORMAL:</strong> Si el cliente se presenta con Señor(a), Licenciado(a), etc., seguido de su nombre/apellido, dirígete a él/ella de esa misma forma. Si se refiere a ti como Señor(ita)/Joven, dirígete como Señor(a) o Señorita." },
                    { title: "Conoce a tu cliente", content: "Revisa su servicio contratado e historial de incidencias en nuestro CRM para contextualizar la llamada." },
                    { title: "Sé claro y conciso", content: "Utiliza términos simples para explicarle al cliente lo que está pasando con su servicio." },
                    { title: "Deriva solo si es necesario", content: "Trata de resolver los problemas del cliente en un primer contacto." }
                ]
            },
            {
                section: "2. ABC PERÚ FIBRA",
                icon: "ph-book-open-text",
                cards: [
                    { title: "Cable Drop", content: "Cable que se conecta a los puertos de la CTO e ingresa al domicilio del cliente." },
                    { title: "Cable ethernet / LAN / RJ45", content: "Cable de red que nos permite conectar el router a nuestros dispositivos de manera directa." },
                    { title: "Caja / CTO", content: "Caja que protege los empalmes de fibra entre la red principal y el domicilio de los clientes." },
                    { title: "Dirección IP / Protocolo de Internet", content: "Número que identifica nuestro dispositivo en Internet." },
                    { title: "DNS", content: "Sistema de nombres de dominio. Funciona como la guía telefónica en Internet. Ubica las IP de los servidores (ejemplo: Facebook.com)." },
                    { title: "IP Dinámica", content: "IP pública que cambia cada cierto tiempo." },
                    { title: "IP Estática", content: "IP pública que no cambia, siempre será la misma." },
                    { title: "IP Privada", content: "Direcciones que identifican a nuestro router y dispositivos conectados a él." },
                    { title: "IP Pública", content: "Dirección que identifica a mi router, como mi dispositivo principal de cara a la red de internet. También identifica servidores en internet." },
                    { title: "Jumper / Cable amarillo / Patch Cord", content: "Cable que conecta al cable Drop en la roseta con la ONT del cliente." },
                    { title: "NAT (Network Address Translation)", content: "Traducción de direcciones de red. Procedimiento que vincula tu IP privada a la IP Pública otorgada por tu operador para interactuar en Internet." },
                    { title: "Roseta", content: "Caja que protege el empalme entre el cable de fibra de exteriores y el de interiores." },
                    { title: "Router / ONT", content: "Dispositivo que convierte la señal óptica en señal digital en tu router para conectarte a Internet vía cable o WiFi." }
                ]
            },
            {
                section: "3. ABC GAMER",
                icon: "ph-game-controller",
                cards: [
                    { title: "Enrutamiento", content: "Cuando el Gamer ingresa a un juego de la lista, lo conectamos con el servidor más óptimo. Si abre otro, localizamos el mejor servidor automáticamente." },
                    { title: "Lag", content: "Ping elevado, superior al promedio." },
                    { title: "Latencia", content: "Tiempo de respuesta ante una acción en la red, medido en milisegundos." },
                    { title: "Pérdida de paquetes", content: "Cuando el juego se queda congelado por algunos segundos durante la partida." },
                    { title: "Ping", content: "Mide la latencia en milisegundos (ms). El ping promedio va a depender del juego y servidor elegido." },
                    { title: "SDwan", content: "Red de área extensa, definida por software, que gestiona de forma centralizada los componentes de hardware." },
                    { title: "Servidor", content: "Lugar donde se puede elegir jugar. Mientras más alejado, mayor será el ping." }
                ]
            },
            {
                section: "4. PROTOCOLO DE LLAMADA",
                icon: "ph-phone-call",
                cards: [
                    { 
                        title: "1. Saludo Inicial (Bienvenida)", 
                        content: "TEMPL" 
                    },
                    { title: "2. Confirmación del Motivo", content: "<div class='text-pf-red font-semibold mb-2'>Opciones:</div><div class='flex flex-col gap-3'><div class='bg-gray-100 p-4 rounded-2xl text-gray-700'>- Cuéntame, ¿en qué te puedo ayudar el día de hoy?</div><div class='bg-gray-100 p-4 rounded-2xl text-gray-700'>- ¿Cómo te puedo ayudar?</div></div><em class='text-gray-500 block mt-4 text-sm'>*Validar el motivo de la llamada, puedes parafrasear lo mencionado por el cliente.</em>" },
                    { 
                        title: "3. Solicitar Datos de la Cuenta", 
                        content: "TEMPL" 
                    },
                    { 
                        title: "4. Preguntas de Sondeo", 
                        content: "TEMPL" 
                    },
                    { 
                        title: "5. Solución y Contexto", 
                        content: "TEMPL" 
                    },
                    { 
                        title: "6. Cierre Positivo", 
                        content: "TEMPL" 
                    },
                    { title: "7. Derivación Encuesta", content: "<div class='bg-gray-100 p-4 rounded-2xl text-gray-700'>Al finalizar la llamada recibirá una breve encuesta para calificar la atención. 'Gracias por llamar a Perú Fibra' (OBLIGATORIO).</div><em class='text-gray-500 block mt-4 text-sm'>*Nota: Enviar encuesta</em>" }
                ],
                quickAccess: [
                    { 
                        title: "LINEAMIENTOS DE MANEJO DEL TIEMPO", 
                        content: "",
                        subItems: [
                            {
                                title: "CANAL VOZ",
                                icon: "ph-phone-call",
                                isModal: true,
                                content: "TEMPL"
                            },
                            {
                                title: "CANAL DIGITAL",
                                icon: "ph-chat-circle-dots",
                                isModal: true,
                                content: "TEMPL"
                            }
                        ]
                    },
                    { 
                        title: "VALIDACIÓN DE NÚMERO DE CONTACTO", 
                        icon: "ph-phone-call",
                        isModal: true,
                        content: "TEMPL"
                    },
                    {
                        title: "VALIDACIÓN DE CORREO ELECTRÓNICO",
                        icon: "ph-envelope",
                        isModal: true,
                        content: "TEMPL"
                    },
                    {
                        title: "SOLICITUD DE DATOS",
                        icon: "ph-clipboard-text",
                        content: "",
                        subItems: [
                            {
                                title: "PARA CONSULTAS",
                                icon: "ph-chat-circle-dots",
                                isModal: true,
                                content: "TEMPL"
                            },
                            {
                                title: "PARA INFORMACIÓN CONFIDENCIAL",
                                icon: "ph-lock-key",
                                isModal: true,
                                content: "TEMPL"
                            },
                            {
                                title: "PARA VARIACIÓN EN CONTRATO",
                                icon: "ph-file-text",
                                isModal: true,
                                content: "TEMPL"
                            }
                        ]
                    },
                    {
                        title: "PREGUNTAS DE VALIDACIÓN Y SEGURIDAD",
                        icon: "ph-lock-key",
                        isModal: true,
                        content: "TEMPL"
                    },
                    {
                        title: "SEGURIDAD DE LA INFORMACIÓN",
                        icon: "ph-shield-check",
                        isModal: true,
                        content: "TEMPL"
                    },
                    {
                        title: "RETENCIÓN: CLIENTE SOLICITA BAJA",
                        content: "",
                        subItems: [
                            {
                                title: "CLIENTE SOLICITA BAJA",
                                icon: "ph-user-minus",
                                isModal: true,
                                content: "TEMPL"
                            },
                            {
                                title: "BAJA TITULAR FALLECIDO",
                                icon: "ph-user-circle-minus",
                                isModal: true,
                                content: "TEMPL"
                            },
                            {
                                title: "TITULAR EN EL EXTRANJERO O INCAPACITADO",
                                icon: "ph-airplane-tilt",
                                isModal: true,
                                content: "TEMPL"
                            },
                            {
                                title: "DESISTE DE CANCELACIÓN",
                                icon: "ph-check-circle",
                                isModal: true,
                                content: "TEMPL"
                            }
                        ]
                    },
                    {
                        title: "PROBLEMAS CON CÓDIGO DE VERIFICACIÓN POR SMS",
                        icon: "ph-device-mobile",
                        isModal: true,
                        content: "TEMPL"
                    },
                    {
                        title: "RECOJO DE EQUIPOS",
                        icon: "ph-package",
                        isModal: true,
                        content: "TEMPL"
                    },
                    {
                        title: "CLIENTE DESEA ACTUALIZAR SUS DATOS",
                        icon: "ph-pencil-simple",
                        isModal: true,
                        content: "TEMPL"
                    },
                    {
                        title: "CAMBIO DE PLAN (DOWNGRADE / UPGRADE)",
                        icon: "ph-arrows-left-right",
                        isModal: true,
                        content: "TEMPL"
                    },
                    {
                        title: "GESTIÓN TÉCNICA",
                        icon: "ph-wrench",
                        isModal: false,
                        content: "",
                        subItems: [
                            {
                        title: "PÉRDIDA DEL SERVICIO",
                        icon: "ph-wifi-slash",
                        isModal: true,
                        content: "TEMPL"
                    },
                    {
                        title: "AGENDAMIENTO VISITA TÉCNICA",
                        icon: "ph-calendar-plus",
                        isModal: true,
                        content: "TEMPL"
                    },
                    {
                        title: "AGENDAMIENTO VT CLIENTE CRÍTICO",
                        icon: "ph-warning-octagon",
                        isModal: true,
                        content: "TEMPL"
                    },
                    {
                        title: "TRANSFERENCIA HACIA AT",
                        icon: "ph-phone-transfer",
                        isModal: true,
                        content: "TEMPL"
                    },
                    {
                        title: "CANCELACIÓN ES VT POR PEXT",
                        icon: "ph-wrench",
                        isModal: true,
                        content: "TEMPL"
                    },
                    {
                        title: "CLIENTE REPORTA MAL CABLEADO / CABLE EXTERIOR COLGADO / QUEJAS DE VECINOS",
                        icon: "ph-warning",
                        isModal: true,
                        content: "TEMPL"
                    },
                    {
                        title: "SOPORTE SERVICIOS TV",
                        icon: "ph-television",
                        isModal: true,
                        content: "TEMPL"
                    },
                    {
                        title: "CLIENTE SOLICITA SOPORTE PARA APP DE TV",
                        icon: "ph-device-mobile-camera",
                        isModal: true,
                        content: "TEMPL"
                            }
                        ]
                    },
                    {
                        title: "CLIENTE REPORTA CONTRATACIÓN NO RECONOCIDA",
                        icon: "ph-prohibit",
                        isModal: true,
                        content: "TEMPL"
                    },
                    {
                        title: "PLAN INCORRECTO DESDE LA VENTA",
                        icon: "ph-file-text",
                        isModal: true,
                        content: "TEMPL"
                    },
                    {
                        title: "SOLICITUD DE MESH",
                        icon: "ph-wifi-high",
                        isModal: true,
                        content: "TEMPL"
                    }
                ]
            },
            {
                section: "5. PROTOCOLO DE CLIENTE DIFICIL",
                icon: "ph-user-warning",
                cards: [
                    { 
                        title: "Llamada Vicio", 
                        content: "TEMPL" 
                    },
                    { 
                        title: "Llamada Reiterativa", 
                        content: "TEMPL"
                    },
                    { 
                        title: "Queja o Apelación", 
                        content: "TEMPL"
                    },
                    { 
                        title: "Cliente Incómodo Desea Reclamar", 
                        content: "TEMPL"
                    },
                    { 
                        title: "Cliente Ofensivo", 
                        content: "TEMPL"
                    },
                    { 
                        title: "Devolución de Llamada", 
                        content: "TEMPL"
                    }
                ]
            },
            {
                section: "6. PROTOCOLO DE CONTINGENCIAS",
                icon: "ph-warning-octagon",
                cards: [
                    { 
                        title: "Problemas Masivos", 
                        content: "TEMPL"
                    },
                    { 
                        title: "Caída Masiva de Aplicativos Internos / Saturación", 
                        content: "TEMPL"
                    },
                    { 
                        title: "Limpieza de Cableado Aéreo", 
                        content: "TEMPL"
                    },
                    { 
                        title: "Derivación a Persona No Tecnológica", 
                        content: "TEMPL"
                    },
                    { 
                        title: "Mala Gestión en Otros Puntos de Contacto", 
                        content: "TEMPL"
                    },
                    { 
                        title: "Deuda en el Predio", 
                        content: "TEMPL"
                    },
                    { 
                        title: "Caída de Aplicativos Externos", 
                        content: "TEMPL"
                    },
                    { 
                        title: "Problema Página de Reclamos", 
                        content: "TEMPL"
                    },
                    { 
                        title: "Sin Cobertura", 
                        content: "TEMPL"
                    },
                    { 
                        title: "Error de Facturación Masivo", 
                        content: "TEMPL"
                    },
                    { 
                        title: "Cliente Revendedor", 
                        content: "TEMPL"
                    },
                    { 
                        title: "Call Out a Usuarios No Atendidos", 
                        content: "TEMPL"
                    }
                ]
            },
            {
                section: "7. PROTOCOLO DE GESTIONES",
                icon: "ph-wrench",
                content: "TEMPL"
            },
            {
                section: "8. PROTOCOLO DE FACTURACIÓN",
                icon: "ph-receipt",
                content: "TEMPL"
            },
            {
                section: "9. POLÍTICA DE ESCALACIÓN SUPERVISOR",
                icon: "ph-users-three",
                cards: [
                    { title: "Lineamientos de Escalación", content: "Validar razón, intentar resolver (FCR) y agotar herramientas antes de escalar. Explicar qué sí se puede hacer.<br>Solo transferir si el cliente <strong>insiste</strong>. No incentivar la escalación." },
                    { title: "Protocolo de Transferencia", content: "<strong>Sup Disponible:</strong> 'Voy a coordinar con mi supervisión...' y transferir.<br><strong>Sup NO Disponible:</strong> Registrar en CRM. Informar contacto máx 24 horas hábiles." },
                    { title: "Prohibiciones", content: "NUNCA decir 'no hay supervisores' sin dar alternativa. NUNCA colgar o evitar. NUNCA transferir sin contexto al supervisor." }
                ]
            },
            {
                section: "10. CAMBIO DE TITULARIDAD / FORMATOS",
                icon: "ph-file-text",
                cards: [
                    { title: "Requisitos Cambio Titularidad / Cesión", content: "Antiguo titular debe estar al día (1er recibo pagado).<br><strong>Requisitos:</strong><br>- Correo y teléfono del NUEVO titular (no pueden ser los mismos).<br>- Copia DNI Vigente (ambas caras) de ambos.<br>- Formato de cesión firmado a mano.<br>- Vigencia de poderes (empresa, max 3 meses).<br>El formato llega al correo, 48hrs hábiles para enviarlo." },
                    { title: "Formato de Cesión (RUC a RUC)", content: "Contrato de Cesión de Posición Contractual. El documento no debe presentar manchas, firmado por ambos, firmas a mano similares al DNI." },
                    { title: "Formato de Cesión (RUC a DNI)", content: "Aplica de Persona Jurídica (LA CEDENTE) a Persona Natural (LA CESIONARIA). Mismas reglas de llenado." },
                    { title: "Formato de Cesión (DNI a RUC)", content: "Aplica de Persona Natural (LA CEDENTE) a Persona Jurídica (LA CESIONARIA). Mismas reglas de llenado." },
                    { title: "Formato de Cesión (DNI a DNI)", content: "Aplica entre Personas Naturales. Ambos llenan sus datos, DNI, dirección e incluyen fecha de instalación original." },
                    { title: "Constancia de No Adeudo", content: "Documento emitido por Perú Fibra certificando que el cliente con DNI [X] no registra deuda vigente o pendiente de pago." }
                ]
            }
        ];

        // --- LOGIC & INTERACTIVITY ---
        var currentCategory = 'all';
        var searchQuery = '';

        var indexMenu = document.getElementById('indexMenu');
        var cardsGrid = document.getElementById('cardsGrid');
        var searchInput = document.getElementById('searchInput');
        var clearSearchBtn = document.getElementById('clearSearchBtn');
        var sectionTitle = document.getElementById('sectionTitle');
        var sectionDesc = document.getElementById('sectionDesc');
        var emptyState = document.getElementById('emptyState');
        var resultCount = document.getElementById('resultCount');
        
        // Global state to track expanded cards (can be useful if you want to keep them open across searches)
        // Set to empty for now. If we want them closed by default, we just don't add the 'expanded' class initially.

        // Mobile Sidebar controls
        var sidebar = document.getElementById('sidebar');
        var mobileMenuBtn = document.getElementById('mobileMenuBtn');
        var closeSidebarBtn = document.getElementById('closeSidebarBtn');

        function toggleSidebar() {
            sidebar.classList.toggle('-translate-x-full');
        }
        mobileMenuBtn.addEventListener('click', toggleSidebar);
        closeSidebarBtn.addEventListener('click', toggleSidebar);
        
        // Toggle card expansion
        function toggleCard(buttonElement) {
            var wrapper = buttonElement.nextElementSibling;
            var icon = buttonElement.querySelector('.expand-icon');
            
            wrapper.classList.toggle('expanded');
            icon.classList.toggle('expanded-icon');
        }

        // Highlight function for search terms
        function highlightText(text, query) {
            if (!query) return text;
            // Escape regex chars
            var escapedQuery = query.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
            var regex = new RegExp("TEMPL", 'gi');
            return text.replace(regex, '<mark>$1</mark>');
        }

        function renderSidebar() {
            indexMenu.innerHTML = "TEMPL";

            protocolData.forEach(function(section, index) { return  {
                var isActive = currentCategory === index };
                var activeClass = isActive ? 'bg-red-50 text-pf-red' : 'text-gray-700 hover:bg-gray-100';
                
                indexMenu.innerHTML += "TEMPL";
            });
        }
        
        var activeQaSubItems = null;
        var activeQaParentTitle = null;

        function openQuickAccess(qaIndex, sectionIndex) {
            var qaItem = protocolData[sectionIndex].quickAccess[qaIndex];
            
            if (qaItem.isModal) {
                openModal("TEMPL", qaItem.content);
                return;
            }

            document.getElementById('cardsGrid').classList.add('hidden');
            if(document.getElementById('emptyState')) document.getElementById('emptyState').classList.add('hidden');
            var qaView = document.getElementById('quickAccessView');
            qaView.classList.remove('hidden');
            
            document.getElementById('qaTitle').innerText = qaItem.title;
            
            if (qaItem.subItems) {
                activeQaSubItems = qaItem.subItems;
                activeQaParentTitle = qaItem.title;
                var firstNonModal = qaItem.subItems.findIndex(function(sub) { return !sub.isModal });
                renderSubItems(firstNonModal !== -1 ? firstNonModal : 0);
            } else {
                activeQaSubItems = null;
                activeQaParentTitle = null;
                document.getElementById('qaContent').innerHTML = qaItem.content || "Contenido pendiente";
                
                var slug = qaItem.title.toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "").replace(/\s+/g, '-');
                history.replaceState(null, '', "TEMPL");
            }
            
            document.getElementById('mainContent').scrollTo({ top: 0, behavior: 'smooth' });
        }

        function renderSubItems(activeIdx) {
            if (!activeQaSubItems) return;
            var qaContent = document.getElementById('qaContent');
            
            var tabsHtml = "TEMPL";
            activeQaSubItems.forEach(function(sub, idx) { return  {
                var isActive = idx === activeIdx && !sub.isModal };
                var activeClasses = isActive 
                    ? 'border-pf-red bg-red-50 text-pf-red shadow-sm ring-1 ring-pf-red' 
                    : 'border-gray-200 bg-white text-gray-700 hover:border-pf-red hover:text-pf-red hover:bg-gray-50';
                
                tabsHtml += "TEMPL";
            });
            tabsHtml += '</div>';
            
            qaContent.innerHTML = tabsHtml + "TEMPL";
            
            // Render initial inline content if not modal
            if (activeQaSubItems[activeIdx] && !activeQaSubItems[activeIdx].isModal) {
                document.getElementById('inlineSubContent').innerHTML = activeQaSubItems[activeIdx].content;
            }
            
            // Set fake deep link
            var slugParent = (activeQaParentTitle || 'seccion').toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "").replace(/\s+/g, '-');
            var slugChild = activeQaSubItems[activeIdx].title.toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "").replace(/\s+/g, '-');
            history.replaceState(null, '', "TEMPL");
        }

        function handleSubItemClick(idx) {
            var sub = activeQaSubItems[idx];
            
            // Set fake deep link
            var slugParent = (activeQaParentTitle || 'seccion').toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "").replace(/\s+/g, '-');
            var slugChild = sub.title.toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "").replace(/\s+/g, '-');
            history.replaceState(null, '', "TEMPL");
            
            if (sub.isModal) {
                openModal("TEMPL", sub.content);
            } else {
                renderSubItems(idx);
            }
        }

        function closeQuickAccess() {
            document.getElementById('quickAccessView').classList.add('hidden');
            document.getElementById('cardsGrid').classList.remove('hidden');
            history.replaceState(null, '', window.location.pathname);
        }

        function filterByCategory(categoryIndex) {
            currentCategory = categoryIndex;
            // On mobile, close sidebar after clicking
            if(window.innerWidth < 768) {
                sidebar.classList.add('-translate-x-full');
            }
            renderSidebar();
            renderCards();
        }

        function resetView() {
            searchInput.value = '';
            searchQuery = '';
            clearSearchBtn.classList.add('hidden');
            filterByCategory('all');
        }

        function clearSearch() {
            searchInput.value = '';
            searchQuery = '';
            clearSearchBtn.classList.add('hidden');
            renderCards();
        }

        function renderCards() {
            if(document.getElementById('quickAccessView')) document.getElementById('quickAccessView').classList.add('hidden');
            if(document.getElementById('cardsGrid')) document.getElementById('cardsGrid').classList.remove('hidden');
            cardsGrid.innerHTML = '';
            var count = 0;

            var dataToRender = protocolData;
            
            // Filter by Category
            if (currentCategory !== 'all') {
                dataToRender = [protocolData[currentCategory]];
                sectionTitle.innerText = protocolData[currentCategory].section;
                sectionDesc.innerText = "Información y protocolos correspondientes a esta sección.";
                
                // Set layout to vertical list globally now
                cardsGrid.className = "flex flex-col gap-4 items-stretch"; 

            } else {
                sectionTitle.innerText = searchQuery ? "Resultados de Búsqueda" : "Todos los Protocolos";
                sectionDesc.innerText = searchQuery ? "TEMPL" : "Explora la base de conocimiento o utiliza el buscador.";
                // Set layout to vertical list globally now
                cardsGrid.className = "flex flex-col gap-4 items-stretch";
            }

            // Iterate and Filter by Search Query
            dataToRender.forEach(function(section, sectionIdx) { return  {
                // If there's a search query }, filter cards within the section
                var filteredCards = (section.cards || []).filter(function(card) { return  {
                    if (!searchQuery }) return true;
                    var searchLower = searchQuery.toLowerCase();
                    return card.title.toLowerCase().includes(searchLower) || card.content.toLowerCase().includes(searchLower);
                });
                
                var filteredQuickAccess = (section.quickAccess || []).map(function(qa, idx) { return ({...qa }, originalIdx: idx})).filter(function(qa) { return  {
                    if (!searchQuery }) return true;
                    var searchLower = searchQuery.toLowerCase();
                    return qa.title.toLowerCase().includes(searchLower) || qa.content.toLowerCase().includes(searchLower);
                });

                // Check if this section has custom raw HTML content instead of cards
                var hasCustomContent = section.content && (!searchQuery || section.content.toLowerCase().includes(searchQuery.toLowerCase()));

                if (filteredCards.length > 0 || filteredQuickAccess.length > 0 || hasCustomContent) {
                    // Create Section Header (only if showing all or multiple sections might show up in search)
                    if (currentCategory === 'all') {
                        var sectionHeader = document.createElement('div');
                        sectionHeader.className = "col-span-1 md:col-span-2 xl:col-span-3 mt-6 mb-2";
                        sectionHeader.innerHTML = "TEMPL";
                        cardsGrid.appendChild(sectionHeader);
                    }
                    
                    if (hasCustomContent) {
                        count++;
                        var contentEl = document.createElement('div');
                        contentEl.className = "col-span-1 md:col-span-2 xl:col-span-3 mb-6 w-full";
                        contentEl.innerHTML = section.content;
                        cardsGrid.appendChild(contentEl);
                    }

                    filteredCards.forEach(function(card) { return  {
                        count++ };
                        var cardEl = document.createElement('div');
                        
                        // New Global Styling: Long capsule, rounded corners, red border, collapsible
                        cardEl.className = "protocol-card bg-white rounded-3xl shadow-sm border border-gray-200 flex flex-col border-l-8 border-l-pf-red w-full overflow-hidden"; 
                        
                        // Default expanded state based on search. If searching, expand to show context.
                        var isExpandedClass = searchQuery ? 'expanded' : '';
                        var isIconRotated = searchQuery ? 'expanded-icon' : '';

                        cardEl.innerHTML = "TEMPL";
                        
                        cardsGrid.appendChild(cardEl);
                    });
                    
                    if (filteredQuickAccess.length > 0) {
                        var qaHeader = document.createElement('div');
                        qaHeader.className = "col-span-1 md:col-span-2 xl:col-span-3 mt-8 mb-4";
                        qaHeader.innerHTML = "TEMPL";
                        cardsGrid.appendChild(qaHeader);

                        var qaGrid = document.createElement('div');
                        qaGrid.className = "col-span-1 md:col-span-2 xl:col-span-3 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4 w-full";
                        
                        filteredQuickAccess.forEach(function(qa) { return  {
                            count++ };
                            var btn = document.createElement('button');
                            btn.className = "bg-white border border-gray-200 hover:border-pf-red hover:shadow-md transition-all duration-200 rounded-xl p-4 flex flex-col items-center justify-center text-center group min-h-[100px]";
                            
                            // Determine actual section index if we are viewing all or specific
                            var actualSectionIdx = currentCategory === 'all' ? sectionIdx : currentCategory;
                            
                            btn.innerHTML = "TEMPL";
                            btn.onclick = function() { return openQuickAccess(qa.originalIdx }, actualSectionIdx);
                            qaGrid.appendChild(btn);
                        });
                        cardsGrid.appendChild(qaGrid);
                    }
                }
            });

            // UI State updates based on results
            if (count === 0) {
                emptyState.classList.remove('hidden');
                cardsGrid.classList.add('hidden');
                resultCount.classList.add('hidden');
            } else {
                emptyState.classList.add('hidden');
                cardsGrid.classList.remove('hidden');
                
                if (searchQuery) {
                    resultCount.classList.remove('hidden');
                    resultCount.innerText = "TEMPL";
                } else {
                    resultCount.classList.add('hidden');
                }
            }
        }

        // Search event listener
        searchInput.addEventListener('input', function(e) { return  {
            searchQuery = e.target.value.trim( });
            
            if (searchQuery.length > 0) {
                clearSearchBtn.classList.remove('hidden');
                // Automatically switch to 'all' categories when searching globally for better UX
                if (currentCategory !== 'all') {
                    currentCategory = 'all';
                    renderSidebar();
                }
            } else {
                clearSearchBtn.classList.add('hidden');
            }
            
            renderCards();
        });

        // Initialization
        window.addEventListener('DOMContentLoaded', function() { return  {
            renderSidebar( });
            renderCards();
        });

        // Modal Logic
        function openModal(title, contentHtml) {
            document.getElementById('globalModalTitle').innerHTML = title;
            document.getElementById('globalModalContent').innerHTML = contentHtml;
            var modal = document.getElementById('globalModal');
            modal.classList.remove('hidden');
            // Trigger animation
            setTimeout(function() { return  {
                modal.classList.remove('opacity-0' });
                modal.firstElementChild.classList.remove('scale-95');
                modal.firstElementChild.classList.add('scale-100');
            }, 10);
            
            document.addEventListener('keydown', handleEsc);
        }

        function closeModal() {
            var modal = document.getElementById('globalModal');
            modal.classList.add('opacity-0');
            modal.firstElementChild.classList.remove('scale-100');
            modal.firstElementChild.classList.add('scale-95');
            setTimeout(function() { return  {
                modal.classList.add('hidden' });
            }, 300);
            document.removeEventListener('keydown', handleEsc);
        }
        
        function handleEsc(e) {
            if (e.key === 'Escape') closeModal();
        }

    