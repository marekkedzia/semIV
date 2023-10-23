# Specyfikacja wymagań dla systemu Discovery AGD

## Wstęp

Discovery AGD zajmuje się wypożyczaniem sprzętu AGD w całym Wrocławiu. Celem projektu jest stworzenie systemu do zarządzania i zamawiania sprzętu AGD, który ułatwi pracę wewnątrz firmy oraz zwiększy zadowolenie klientów.

## Historyjki użytkowników

### Historyjka użytkownika 1

**Tytuł**: Przeglądanie dostępnych sprzętów AGD

**Jako** gość  
**chcę** mieć możliwość przeglądania dostępnych sprzętów AGD  
**aby** zapoznać się z ofertą Discovery AGD

**Kryterium akceptacji**: Wyświetlanie listy dostępnych sprzętów AGD z cenami i opisami.

### Historyjka użytkownika 2

**Tytuł**: Składanie i opłacanie zamówienia online

**Scenariusz**: Składanie i opłacanie zamówienia  
**Given** zalogowany klient  
**And** wybrany sprzęt AGD do wynajęcia  
**When** klient składa zamówienie  
**Then** zamówienie zostaje zarejestrowane  
**And** klient zostaje przekierowany do procesu płatności

**Jako** klient  
**chcę** mieć możliwość złożenia i opłacenia zamówienia online  
**aby** wynająć sprzęt AGD w prosty i wygodny sposób

**Kryterium akceptacji**:  
- Możliwość wyboru i dodania sprzętu AGD do koszyka
- Przejście przez proces płatności (karta, blik, przelew tradycyjny)

### Historyjka użytkownika 3

**Tytuł**: Dostęp do historii zamówień

**Jako** klient  
**chcę** mieć dostęp do historii swoich zamówień  
**aby** móc śledzić swoje wypożyczenia i opłaty

**Kryterium akceptacji**: Wyświetlanie listy zamówień klienta z informacjami o dacie, sprzęcie AGD i opłaconej kwocie.

### Historyjka użytkownika 4

**Tytuł**: Edycja informacji o zamówieniach i zmiana statusu

**Scenariusz**: Edycja zamówienia przez administratora  
**Given** zalogowany administrator  
**And** istniejące zamówienie  
**When** administrator edytuje dane zamówienia lub zmienia jego status  
**Then** zmiany zostają zapisane

**Jako** administrator  
**chcę** mieć możliwość edycji informacji o zamówieniach oraz zmiany ich statusu  
**aby** zarządzać zamówieniami klientów

**Kryterium akceptacji**:  
- Możliwość zmiany danych zamówienia (np. adres dostawy, data wypożyczenia)
- Możliwość zmiany statusu zamówienia (np. "złożone", "rozpatrzone")
### Historyjka użytkownika 5

**Tytuł**: Filtrowanie listy zamówień

**Jako** administrator  
**chcę** móc filtrować listę zamówień  
**aby** łatwo znaleźć interesujące mnie zamówienia

**Kryterium akceptacji**: Możliwość filtrowania listy zamówień po dacie, statusie, sprzęcie AGD itp.

### Historyjka użytkownika 6

**Tytuł**: Edycja daty zamówienia

**Scenariusz**: Edycja daty zamówienia  
**Given** zalogowany klient  
**And** istniejące zamówienie  
**When** klient edytuje datę zamówienia  
**Then** zmiany zostają zapisane

**Jako** klient  
**chcę** mieć możliwość edycji daty zamówienia  
**aby** dostosować wypożyczenie sprzętu AGD do swoich potrzeb

**Kryterium akceptacji**:  
- Możliwość zmiany daty wypożyczenia oraz zwrotu sprzętu AGD
- Możliwość edycji daty zamówienia maksymalnie jeden dzień przed dostawą

### Historyjka użytkownika 7

**Tytuł**: Otrzymywanie powiadomienia e-mail z potwierdzeniem zamówienia

**Jako** klient  
**chcę** otrzymać powiadomienie e-mail z potwierdzeniem zamówienia  
**aby** mieć pewność, że moje zamówienie zostało przyjęte

**Kryterium akceptacji**: Wysyłanie e-maila z potwierdzeniem zamówienia do klienta po złożeniu i opłaceniu zamówienia

